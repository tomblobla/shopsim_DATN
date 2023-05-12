from django.urls import path
from . import views

urlpatterns = [
    path('dang-ky/', views.signup, name = 'signup'),
    path('dang-nhap/', views.login_view, name = 'signin'),
    path('thay-doi-thong-tin/', views.customer_update, name='customer_update'),
    path('thay-doi-mat-khau/', views.change_password, name='pass-change'),
    path('gio-hang/', views.cart, name='cart'),
    path('them-vao-gio-hang/', views.add_to_cart, name='add-to-cart'),
    path('bo-khoi-gio-hang/', views.remove_from_cart, name='remove-from-cart'),
    path('kich-hoat/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('gui-lai-email-xac-nhan/<slug:username>', views.resend_valid_mail, name = 'resend-email-valid'),
    path('dang-xuat/', views.logout_view, name='logout'),
    path('reset-password/', 
        views.CustomPasswordResetView.as_view(),
        name='password-reset'),
    path('reset-password/hoan-thanh/',
        views.CustomPasswordResetDoneView.as_view(), 
        name='password_reset_done'),
    path('reset-password-xac-nhan/<uidb64>/<token>/',
        views.CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path('reset-password-hoan-thanh/',
        views.CustomPasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
]