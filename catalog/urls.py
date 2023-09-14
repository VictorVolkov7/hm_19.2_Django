from django.urls import path

from catalog.views import home_page, contact_info

urlpatterns = [
    path('', home_page, name='home_page'),
    path('contact/', contact_info, name='contact_info')

]
