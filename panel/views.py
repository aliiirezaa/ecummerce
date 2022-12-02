from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from products.models import Products
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .mixins import FieldsMixin,AccessAuthorMixin, FormVlidMixin, SuperUserMixin, AccessAuthorsMixin
from .forms import ProfileForm
# Create your views here.
User = get_user_model()

def panel_page(request):
    return render(request, 'panel/home.html')

class ProductsListView(ListView):
    model=Products
    context_object_name = 'products'
    template_name ='panel/products_list.html'
    paginate_by= 3
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Products.objects.all()
        
        return Products.objects.filter(author=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.get_queryset()
        paginator = Paginator(query, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            products = paginator.get_page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        
        context['object_list']=products
        return context
    
    
class ProductCreateView(AccessAuthorsMixin, FormVlidMixin, FieldsMixin, CreateView):
    model=Products
    success_url= reverse_lazy('panel:products_list')
    template_name = 'panel/create_product.html'
    
class ProductsUpdateView(AccessAuthorMixin,FormVlidMixin, FieldsMixin, UpdateView):
    model=Products 
    template_name = 'panel/create_product.html'
    success_url= reverse_lazy('panel:products_list')

class ProductsDeleteView(SuperUserMixin, DeleteView):
    model=Products 
    success_url = reverse_lazy('panel:products_list')
    template_name = 'panel/confirm_delete_product.html'
    

class ProfileView(UpdateView):
    model = User 
    form_class = ProfileForm
    template_name = 'panel/profile.html'
    
    def get_success_url(self):
        return reverse_lazy('panel:profile', kwargs={'pk':self.object.pk}) 
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user':self.request.user
        })
        return kwargs