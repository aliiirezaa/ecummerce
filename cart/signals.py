from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver 
from .models import Orders, Cart 

@receiver(post_save, sender=Orders)
def order_handler(sender, instance,created, **kwargs):
    try:
        query = Cart.objects.filter(user=instance.user)
        if query.exists():
            cart = query.first()
            cart.orders.add(instance)
            cart.save()
            
        else:
            cart = Cart.objects.create(user=instance.user)
            cart.orders.add(instance)
            cart.save()
    except Cart.DoesNotExist:
        return None
    
@receiver(post_delete, sender=Orders)
def order_delete_handler(sender, instance, **kwargs):
    try:
        query = Cart.objects.filter(user=instance.user)
        if query.exists():
            cart = query.first()
            cart.orders.remove(instance)
            print('\n remmove .... \n')
            cart.save()
            if cart.orders.count() == 0 :
                cart.delete()
                print('\n delete .... \n')
    except Cart.DoesNotExist:
        return None

        