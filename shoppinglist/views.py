from django.shortcuts import render

from django.views.generic import ListView
from .models import Item
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .forms import ItemBuy, ItemIDForm, ItemForm
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