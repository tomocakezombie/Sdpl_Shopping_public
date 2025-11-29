from django.urls import path

from .views import (
    ItemList,
    ItemAddview,
    ItemEditView,
    ItemDeleteView,
    ItemShowView,
    ItemToggleBuyView,
)


app_name='shoppinglist'
urlpatterns = [
    path('list/',ItemList.as_view(),name='list'),
    path('show/', ItemShowView.as_view(), name='show'),
    path('edit/<int:pk>/', ItemEditView.as_view(), name='edit'),
    path('delete/<int:pk>', ItemDeleteView.as_view(), name='delete'),
    path('add/', ItemAddview.as_view(), name='add'),
    path('toggle_buy/<int:pk>/', ItemToggleBuyView.as_view(), name='toggle_buy'),
]
