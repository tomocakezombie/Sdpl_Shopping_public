from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, DeleteView
from django.views.generic.edit import UpdateView  # T23CS044課題（改善ポイント2で使用）
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from .models import Item, Shop
from .forms import ItemBuy, ItemForm, ItemIdForm



class ItemList(LoginRequiredMixin, ListView):
    model = Item
    template_name = "shoppinglist/item_list.html"
    success_url = reverse_lazy("shoppinglist:list")
    login_url = reverse_lazy("accounts:login")

    allowed_sort_fields = ["id", "name", "count", "buy_date", "buy"]
    buy_filter_map = {"true": True, "false": False}
    buy_filter_options = (
        ("all", "すべて"),
        ("true", "購入済み"),
        ("false", "未購入"),
    )

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        item_status = request.POST.get('item_status')
        item = get_object_or_404(Item, pk=item_id)
        item.buy = item_status
        item.save()
        return HttpResponseRedirect(reverse('shoppinglist:list'))
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_param = self.request.GET.get("buy", "all")

        if filter_param in self.buy_filter_map:
            queryset = queryset.filter(buy=self.buy_filter_map[filter_param])

        sort_param = self.request.GET.get("sort")

        if sort_param:
            ordering = sort_param
            if sort_param.startswith("-"):
                field_name = sort_param[1:]
            else:
                field_name = sort_param

            if field_name in self.allowed_sort_fields:
                return queryset.order_by(ordering)

        return queryset.order_by("id")
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form'] = ItemBuy()
        current_sort = self.request.GET.get("sort", "id")
        context['current_sort'] = current_sort
        filter_param = self.request.GET.get("buy", "all")
        if filter_param not in self.buy_filter_map and filter_param != "all":
            filter_param = "all"
        context['current_buy_filter'] = filter_param
        context['buy_filter_options'] = self.buy_filter_options
        sort_toggle = {}
        for field in self.allowed_sort_fields:
            sort_toggle[field] = field
            if current_sort == field:
                sort_toggle[field] = f"-{field}"
            elif current_sort == f"-{field}":
                sort_toggle[field] = field
        context['sort_toggle'] = sort_toggle
        return context


class ItemToggleBuyView(LoginRequiredMixin, View):
    login_url = reverse_lazy("accounts:login")

    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        buy_value = request.POST.get("buy")
        item.buy = (buy_value == "True")
        item.save()
        return redirect("shoppinglist:list")

    
class ItemShowView(LoginRequiredMixin, TemplateView):
    model = Item
    template_name = 'shoppinglist/item_show.html'
    login_url = reverse_lazy("accounts:login")
    
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

class ItemEditView(LoginRequiredMixin, UpdateView):#T23CS044課題（改善ポイント2）
    model = Item
    fields = ['name','item_url','count','buy_date','buy']
    template_name = 'shoppinglist/item_edit.html'
    success_url = reverse_lazy('shoppinglist:list')
    login_url = reverse_lazy("accounts:login")
    
class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'shoppinglist/item_delete.html'
    success_url = reverse_lazy('shoppinglist:list') 
    login_url = reverse_lazy("accounts:login")

class ItemAddview(LoginRequiredMixin, CreateView):
    model = Item

    fields = ['name', 'item_url', 'count', 'buy_date', 'shop']
    template_name = "shoppinglist/item_add.html"
    success_url = reverse_lazy("shoppinglist:list")
    login_url = reverse_lazy("accounts:login")

class ItemUrlView(LoginRequiredMixin, TemplateView):
    model = Item
    template_name = 'shoppinglist/item_url.html'
    login_url = reverse_lazy("accounts:login")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_id = self.kwargs.get('pk')
        item = get_object_or_404(Item, pk=item_id)
        context['item'] = item
        return context
    
class ShopAddView(LoginRequiredMixin, CreateView):
    model = Shop
    fields = ['name', 'shop_site']
    template_name = "shoppinglist/shop_add.html"
    success_url = reverse_lazy("shoppinglist:list")
    login_url = reverse_lazy("accounts:login")
    
class ShopUrlView(TemplateView):
    model = Shop
    template_name = 'shoppinglist/shop_url.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop_id = self.kwargs.get('pk')
        shop = get_object_or_404(Shop, pk=shop_id)
        context['shop'] = shop
        return context