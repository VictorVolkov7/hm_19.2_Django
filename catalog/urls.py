from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import home_page, contact_info, product_page

app_name = CatalogConfig.name

urlpatterns = [
    path('', home_page, name='home_page'),
    path('contact/', contact_info, name='contact_info'),
    path('product/<int:pk>/', product_page, name='product_page')
]
