from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, DeleteView
from django.views.generic.edit import UpdateView  # T23CS044課題（改善ポイント2で使用）
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from .models import Item
from .forms import ItemBuy, ItemForm, ItemIdForm



class ItemList(ListView):
    model = Item
    template_name = "shoppinglist/item_list.html"
    success_url = reverse_lazy("shoppinglist:list")

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        item_status = request.POST.get('item_status')
        item = get_object_or_404(Item, pk=item_id)
        item.buy = item_status
        item.save()
        return HttpResponseRedirect(reverse('shoppinglist:list'))
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form'] = ItemBuy()
        return context


class ItemToggleBuyView(View):
    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        buy_value = request.POST.get("buy")
        item.buy = (buy_value == "True")
        item.save()
        return redirect("shoppinglist:list")

    
class ItemShowView(TemplateView):
    model = Item
    template_name = 'shoppinglist/item_show.html'
    
    def post(self, request, *args, **kwargs):
        item_id = self.request.POST.get('item_id')
        item = get_object_or_404(Item, pk=item_id)
        print('item:id=', item.id)
        context = super().get_context_data(**kwargs)
        context['form_id'] = ItemIdForm()
        context['item'] = item
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = ItemIdForm()
        return context

class ItemEditView(UpdateView):#T23CS044課題（改善ポイント2）
    model = Item
    fields = ['name','item_url','count','buy_date','buy']
    template_name = 'shoppinglist/item_edit.html'
    success_url = reverse_lazy('shoppinglist:list')
    
class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'shoppinglist/item_delete.html'
    success_url = reverse_lazy('shoppinglist:list') 

class ItemAddview(CreateView):
    model = Item

    fields = ['name', 'item_url', 'count', 'buy_date', 'shop']
    template_name = "shoppinglist/item_add.html"
    success_url = reverse_lazy("shoppinglist:list")

