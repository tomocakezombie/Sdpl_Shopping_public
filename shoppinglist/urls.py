from django.urls import path

from .views import ItemList, ItemEditView, ItemDeleteView, ItemShowView
from .views import ItemAddview #ItemShowView, ItemEditView, ItemDeleteView


app_name='shoppinglist'
urlpatterns = [
    path('list/',ItemList.as_view(),name='list'),
    path('show/', ItemShowView.as_view(), name='show'),
    path('edit/<int:pk>/', ItemEditView.as_view(), name='edit'),
    path('delete/<int:pk>', ItemDeleteView.as_view(), name='delete'),
    path('add/', ItemAddview.as_view(), name='add'),
]
