from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Toy, News
from cart.models import CartItem


def auth_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    register_form = UserCreationForm()
    login_form = AuthenticationForm()

    if request.method == 'POST':
        if 'register' in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, 'Регистрация прошла успешно!')
                return redirect('home')
            else:
                messages.error(request, 'Ошибка при регистрации.')
        elif 'login' in request.POST:
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, 'Добро пожаловать!')
                return redirect('home')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')

    return render(request, 'main/auth.html', {
        'register_form': register_form,
        'login_form': login_form
    })


from django.db.models import Q

@login_required
def home(request):
    query = request.GET.get('q')
    tag = request.GET.get('tag')

    toys = Toy.objects.all()

    if query:
        toys = toys.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    if tag:
        toys = toys.filter(tags__name__iexact=tag).distinct()

    news_list = News.objects.order_by('-created_at')[:3]

    return render(request, 'main/home.html', {
        'toys': toys,
        'query': query,
        'tag': tag,
        'news_list': news_list,
    })




def logout_view(request):
    logout(request)
    return redirect('auth')


from .models import Toy, News

def index(request):
    query = request.GET.get('q')
    tag = request.GET.get('tag')

    toys = Toy.objects.all()
    if query:
        toys = toys.filter(name__icontains=query)
    if tag:
        toys = toys.filter(tags__name__iexact=tag)

    # последние 3 новости
    news_list = News.objects.order_by('-created_at')[:3]

    return render(request, 'main/home.html', {
        'toys': toys,
        'query': query,
        'tag': tag,
        'news_list': news_list,
    })

def contact(request):
    return render(request, 'main/contact.html')

def about(request):
    return render(request, 'main/about.html')


@login_required
def add_to_cart(request, toy_id):
    toy = get_object_or_404(Toy, id=toy_id)
    
    # Реальное добавление в корзину
    cart_item, created = CartItem.objects.get_or_create(user=request.user, toy=toy)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.info(request, f"Товар '{toy.name}' добавлен в корзину 🛒")
    return redirect('home')


@login_required
def buy_now(request, toy_id):
    toy = get_object_or_404(Toy, id=toy_id)
    messages.success(request, f"Спасибо за покупку! Вы приобрели: {toy.name} 🎉")
    return redirect('home')