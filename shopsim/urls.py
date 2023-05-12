"""shopsim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from. import views
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls',
         'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),
    path('cua-hang/', views.shop, name='cua-hang'),
    path('trang-chu/', views.home, name='trang-chu'),
    path('', views.home, name='home'),
    path('sim/<slug:slug_sim>', views.sim, name='sim'),
    path('tim-sim', views.search_sim, name='search-sim'),
    path('nha-mang/<slug:slug_network>', views.network, name='network'),
    path('sim-so-dep/<slug:slug_tag>', views.tag, name='tag'),
    path('load-more-sim/', views.SIMListView.as_view(), name='load-more-sim'),
    path('filter-sim/', views.SIMFilterListView.as_view(), name='filter-sim'),
    path('tai-khoan/', include('customer.urls')),
    path('don-hang/', include('order.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
