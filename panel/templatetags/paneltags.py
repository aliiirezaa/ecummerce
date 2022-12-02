from django import template
register = template.Library() 

@register.inclusion_tag('panel/templateTags/link.html')
def link(request, link_name, content):
    return{
        'request':request,
        'link_name':link_name,
        'link':f'panel:{link_name}',
        'content':content
    }