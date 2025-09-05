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
    path("get-refund", views.get_refund, name="get_a_refund"),  
    path("update-refund", views.update_status_refund, name="update_refund"), 
    path("update-refund-time", views.update_last_refund, name="update_refund_time"),

    path("v1/predict", views.external_check_refund, name="predict"),
    path("v1/predict-bulk", views.external_check_refund_bulk, name="predict_bulk") 
]