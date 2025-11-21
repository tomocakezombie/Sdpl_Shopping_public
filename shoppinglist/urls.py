from django.urls import path
from .views import ItemList, ItemShowView

app_name='shoppinglist'
urlpatterns = [
    path('list/',ItemList.as_view(),name='list'),
    path('show', ItemShowView.as_view(), name='show'),
]
