import random 
import string 
from django.utils.text import slugify


def generic_random_numb(char=string.digits, size=5):
    return "".join([random.choice(char) for _ in range(size)])

def generic_unique_slugify(instance, slug=None):
    
    if slug:
        slug=slug 
    else:
        
        slug  = slugify(f'{instance.title} - {generic_random_numb()}', allow_unicode=True)
    
    klass = instance.__class__
    qs_exists = klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f'{slug}-{generic_random_numb()}'
        return(generic_unique_slugify(instance, slug=new_slug))
    return slug 
        