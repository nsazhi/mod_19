from django.contrib.admin.templatetags.admin_list import paginator_number
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .forms import UserRegister
from .models import *

# Create your views here.

def index(request):
    return render(request, 'base.html')


def shop(request):
    games = Game.objects.all()
    context = {'games': games}
    return render(request, 'shop.html', context)


def cart(request):
    return render(request, 'cart.html')


def sign_up_by_django(request):
    info = {}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']
            error = check_sign_up(username, password, repeat_password, age)
            if error:
                info['error'] = error
            else:
                Buyer.objects.create(name=username, age=age)
                return HttpResponse(f'Приветствуем, {username}!')
    else:
        form = UserRegister()
    info['form'] = form
    return render(request, 'registration_page.html', info)


def check_sign_up(*args):
    error = None
    username, password, repeat_password, age = args
    for buyer in Buyer.objects.all():
        if username == buyer.name:
            error = 'Пользователь уже существует'
    if age < 18:
        error = 'Вы должны быть старше 18'
    if password != repeat_password:
        error = 'Пароли не совпадают'
    return error


def news(request):
    news = New.objects.all().order_by('date')
    print(news)
    paginator = Paginator(news, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news.html', {'news': page_obj})