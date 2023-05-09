from django.urls import path
from . import views

urlpatterns = [
    path('dang-ky/', views.signup, name = 'signup'),
    path('dang-nhap/', views.login_view, name = 'signin'),
    path('kich-hoat/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('gui-lai-email-xac-nhan/<slug:username>', views.resend_valid_mail, name = 'resend-email-valid'),
    path('dang-xuat/', views.logout_view, name='logout'),
]