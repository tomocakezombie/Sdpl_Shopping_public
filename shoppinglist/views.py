from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView, CreateView, DeleteView
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
        context = super().get_context_data(**kwargs)
        return context



class ItemEditView(TemplateView):
    template_name = "shoppinglist/item_edit.html"

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, pk=item_id)

        item.name = request.POST.get('name')
        item.count = request.POST.get('count')
        item.buy_date = request.POST.get('buy_date')
        item.save()

        return HttpResponseRedirect(reverse('shoppinglist:list'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = ItemIdForm()
        context['form'] = ItemForm()
        return context



class ItemDeleteView(DeleteView):
    model = Item
    template_name = "shoppinglist/item_delete.html"
    success_url = reverse_lazy("shoppinglist:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = ItemIdForm()
        context['form'] = ItemForm()
        return context


class ItemAddview(CreateView):
    model = Item
    fields = ['name', 'item_url', 'count', 'buy_date', 'shop']
    template_name = "shoppinglist/item_add.html"
    success_url = reverse_lazy("shoppinglist:list")
