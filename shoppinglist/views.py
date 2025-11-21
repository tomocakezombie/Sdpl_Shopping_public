from django.shortcuts import render

from django.views.generic import ListView
from .models import Item
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404

from django.views.generic import TemplateView


from .forms import ItemBuy, ItemIDForm, ItemForm, ItemIdForm
from django.views.generic.base import TemplateView

from django.views.generic.edit import CreateView


# Create your views here.

class ItemList(ListView):
    model = Item
    
    def post(self,request,*args,**kwargs):
        item_id = self.request.POST.get('item_id')
        item = get_object_or_404(Item,pk=item_id)
        item_status = self.request.POST.get('item_status')
        item.buy = item_status
        item.save()
        return HttpResponseRedirect(reverse('shoppinglist:list'))
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form'] = ItemBuy()
        return context

    
class ItemShowView(TemplateView):
    model = Item
    template_name = 'shoppinglist/item_show.html'
    
    def post(self, request, *args, **kwargs):
        item_id = self.request.POST.get('item_id')
        item = Item.objects.get(pk=item_id)
        context = super().get_context_data(**kwargs)
        context['form_id'] = ItemIdForm()
        context['item'] = item
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = ItemIdForm()
        return context



class ItemEditView(TemplateView):
    model =Itemtemplete_name ='dhoppinglist/item_edit.html'
    success_url = 'list/'
    
    def post(self, request, *arg, **kwargs):
        item_id = self.request.POST.get('item_id')
        name = self.request.POST.get('name')
        count = self.request.POST.get('count')
        buy_date =self.request.POST.get('buy_date')
        
        item = get_object_or_404(Item, pk=item_id)
        item.name = name
        item.count = count
        item.buy_date = buy_date
        item.save()
        return HttpResponseRedirect(reverse('shoppinglist:list'))
    def get_context_date(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['form_id'] = ItemIDForm()
        context['form'] = ItemForm()
        return context

    
class ItemDeleteView(TemplateView):
    model = Itemtemplate_name = 'shoppingList/item_delete.html'
    
    def post(self, request, *args, **kwargs):
        item_id = self.request.POST.get('item_id')
        item = get_object_or_404(Item, pk=item_id)
        item.delete()
        return HttpResponseRedirect(reverse('shoppingList:List'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ItemIdForm()
        return context
      
class ItemAddview(CreateView):
    model = Item
    fields = {'name', 'item_url', 'count', 'buy_date', 'shop'}
    template_name = 'shoppinglist/item_add.html'
    success_url = reverse_lazy('shoppinglist:list')


