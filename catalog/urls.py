from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contact_info, ProductDetailView, ProductListView, ProductCreateView, BlogListView, \
    BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, ProductUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('contact/', contact_info, name='contact_info'),
]

product_urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='create_product'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
]

blog_urlpatterns = [
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/edit/<slug:slug>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/delete/<slug:slug>/', BlogDeleteView.as_view(), name='blog_delete'),
]

urlpatterns += product_urlpatterns + blog_urlpatterns
