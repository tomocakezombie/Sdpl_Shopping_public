from django.urls import path

from .views import ItemList, ItemEditView, ItemDeleteView
from .views import ItemAddview #ItemShowView, ItemEditView, ItemDeleteView


app_name='shoppinglist'
urlpatterns = [
    path('list/',ItemList.as_view(),name='list'),

    path('edit', ItemEditView.as_view(), name='edit')
    path('delete', ItemDeleteView.as_view(), name='delete'),
    path('add/', ItemAddview.as_view(), name='add'),
    # path('show', ItemShowView.as_view(), name='show'),
    # path('edit', ItemEditView.as_view(), name='edit'),
    # path('delete', ItemDeleteView.as_view(), name='delete'),
]
