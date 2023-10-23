from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Contacts, Blog, Version
from catalog.services import get_cached_category_list


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Главная Safyro's Market"
        category_list = get_cached_category_list()
        context['category_list'] = category_list
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_name = context['object'].name
        context['title'] = f"{product_name} Safyro's Market"
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Создание товара Safyro's Market"
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.has_perm(f'catalog.set_is_published'):
            raise Http404
        return self.object

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Редактирование товара {self.object.title} Safyro's Market"

        SubjectFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = SubjectFormset(instance=self.object)

        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.object.owner != self.request.user:
            product_fields = [f for f in form.fields.keys()]
            for field in product_fields:
                if not self.request.user.has_perm(f'catalog.set_{field}'):
                    del form.fields[field]
        else:
            del form.fields['is_published']
        return form

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Удаление товара {self.object.title} Safyro's Market"
        return context

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.has_perm(f'catalog.set_is_published'):
            raise Http404
        return self.object


class ContactInfo(TemplateView):
    template_name = 'catalog/contact_info.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object'] = Contacts.objects.first()
        context_data['title'] = "Контакты Safyro's Market"
        return context_data

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"{name}({email}):{message}")
        return redirect('catalog:contact_info')


class BlogListView(ListView):
    model = Blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Новости Safyro's Market"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_title = context['object'].title
        context['title'] = f"{blog_title} Safyro's Market"
        return context

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1

        if self.object.count_views == 100:
            self.send_mail()

        self.object.save()
        return self.object

    def send_mail(self):
        subject = f"Пост {self.object.title} достиг 100 просмотров"
        message = 'Поздравляем!!!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['vektorn1212@gmail.com']

        send_mail(subject, message, from_email, recipient_list)


class BlogCreateView(CreateView, PermissionRequiredMixin):
    model = Blog
    fields = ('title', 'body', 'preview', 'date_create', 'is_published')
    permission_required = 'catalog.add_blog'
    success_url = reverse_lazy('catalog:blog_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Создать: Safyro's Market"
        return context

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)


class BlogUpdateView(UpdateView, PermissionRequiredMixin):
    model = Blog
    fields = ('title', 'body', 'preview', 'date_create', 'is_published', 'count_views')
    permission_required = 'catalog.change_blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_title = context['object'].title
        context['title'] = f"Редактировать: {blog_title} Safyro's Market"
        return context

    def get_success_url(self):
        return reverse('catalog:blog_detail', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title[:15])
            new_blog.save()

        return super().form_valid(form)


class BlogDeleteView(DeleteView, PermissionRequiredMixin):
    model = Blog
    permission_required = 'catalog.delete_blog'
    success_url = reverse_lazy('catalog:blog_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_title = context['object'].title
        context['title'] = f"Удалить: {blog_title} Safyro's Market"
        return context
