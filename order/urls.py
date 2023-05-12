from django.urls import path
from . import views

urlpatterns = [
    path('dat-hang/', views.place_order, name = 'place-order'),
    path('tra-cuu/<int:id>/', views.order_tracker, name = 'order-tracker'),
    path('xem-hoa-don/<int:id>/', views.order_pdf, name = 'order-invoice'),
    path('quan-ly-don/', views.manage_order, name = 'manage-order'),
    path('huy-don/', views.cancel_order, name = 'cancel-order'),
]