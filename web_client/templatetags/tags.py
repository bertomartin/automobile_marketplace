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
    return {'post': post, 'request': context.get('request')}


@register.inclusion_tag('homepage/customer/post_details_modal.html')
def load_post_details_modal(post_id):
    return {'post': Post.objects.get(pk=post_id)}


@register.inclusion_tag('homepage/customer/contact_information_modal.html')
def load_seller_contact_information_modal(post_id):
    return {'post': Post.objects.get(pk=post_id)}


@register.inclusion_tag('homepage/customer/customer_inspections.html')
def load_customer_workshop_modal(user):
    inspections = InspectionRequest.objects.filter(
            requesting_customer=user)
    return {'inspections': inspections}


@register.inclusion_tag('homepage/workshop/contractor_inspections.html')
def load_contractor_workshop_modal(user):
    inspections = InspectionRequest.objects.filter(
        responsible_contractor=Contractor.objects.get(
            user_id=user))
    return {'inspections': inspections}


@register.inclusion_tag('homepage/customer/sharing_options.html')
def load_sharing_options(post_id):
    return {'post_id': Post.objects.get(pk=post_id).pk}
