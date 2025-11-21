from django.urls import path
from .views import ItemList, ItemEditView

app_name='shoppinglist'
urlpatterns = [
    path('list/',ItemList.as_view(),name='list'),
    path('edit', ItemEditView.as_view(), name='edit')
]
