from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.handle_login, name="handle_login"), 
    path("total-refund", views.get_total, name="handle_total"), 
    path("items", views.get_all_item, name="handle_item"), 
    path("item", views.get_item, name="get_item"), 
    path("refund", views.manage_refund, name="handle_refund"),
    path("item-refund", views.get_all_refund, name="handle_get_refund"),  
]