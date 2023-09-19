from django.shortcuts import render

from catalog.models import Product, Contacts


def home_page(request):
    latest_product = Product.objects.all()[:5]

    for product in latest_product:
        print(product.name)

    return render(request, 'catalog/home_page.html')


def contact_info(request):
    contacts = Contacts.objects.first()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"{name}({email}):{message}")
    return render(request, 'catalog/contact_info.html', {'contacts': contacts})
