from django.shortcuts import render


def home_page(request):
    return render(request, 'catalog/home_page.html')


def contact_info(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"{name}({email}):{message}")
    return render(request, 'catalog/contact_info.html')
