from django import template

register = template.Library()


@register.inclusion_tag('homepage/customer/post_details_thumbnail.html')
def load_post_thumbnail(post):
    return {'post': post}
