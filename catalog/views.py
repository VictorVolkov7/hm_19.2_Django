from django.shortcuts import render, get_object_or_404

from catalog.models import Product, Contacts


def home_page(request):
    latest_product = Product.objects.all()

    for product in latest_product[:5]:
        print(product.name)

    context = {
        'object_list': latest_product,
        'title': "Главная Safyro's Market",
    }

    return render(request, 'catalog/home_page.html', context)


def contact_info(request):
    contacts_list = Contacts.objects.first()
    context = {
        'object_list': contacts_list,
        'title': "Контакты Safyro's Market"
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"{name}({email}):{message}")
    return render(request, 'catalog/contact_info.html', context)


def product_page(request, pk):
    products_list = get_object_or_404(Product, pk=pk)
    context = {
        'object_list': products_list,
        'title': f"{products_list.name} Safyro's Market"
    }

    return render(request, 'catalog/product_page.html', context)
