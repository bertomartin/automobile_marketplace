from django import template

from web_client.models import (
    Contractor,
    InspectionRequest,
    Post,
)

register = template.Library()


@register.inclusion_tag('homepage/workshop/workshop_main_container.html',
                        takes_context=True)
def workshop_main_container(context):
    inspections = InspectionRequest.objects.filter(
        responsible_contractor=Contractor.objects.get(
            user_id=context['request'].user)).order_by('status')
    return {'requestos': inspections}


@register.inclusion_tag('homepage/admin/admin_main_container.html')
def admin_main_container():
    return


@register.inclusion_tag('homepage/customer/customer_main_container.html',
                        takes_context=True)
def customer_main_container(context):
    posts = Post.objects.all().order_by('-created')
    view_options = 'homepage/customer/view_options.html'
    ad_bar = 'homepage/customer/ad_bar.html'
    parameters = {'context': context,
                  'posts': posts,
                  'view_options': view_options,
                  'ad_bar': ad_bar}
    return parameters


@register.inclusion_tag('homepage/customer/post_details_thumbnail.html',
                        takes_context=True)
def load_post_thumbnail(context, post):
    return {'context': context, 'post': post}


@register.inclusion_tag('homepage/customer/post_details_modal.html')
def load_post_details_modal(post_id):
    return {'post': Post.objects.get(pk=post_id)}
