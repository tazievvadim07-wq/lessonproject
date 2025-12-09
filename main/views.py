from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Toy, News
from cart.models import CartItem
from django.db.models.functions import Lower


def auth_view(request):
    """Комбинированная страница для входа и регистрации."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        if 'login' in request.POST:
            # 🔹 Вход
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')

        elif 'register' in request.POST:
            # 🔸 Регистрация
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                messages.error(request, 'Пароли не совпадают.')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь с таким именем уже существует.')
            else:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                messages.success(request, 'Регистрация прошла успешно!')
                return redirect('home')

    return render(request, 'main/login_register.html')

def home(request):
    query = request.GET.get('q', '').strip().lower()
    tag = request.GET.get('tag', '').strip()

    toys = Toy.objects.all()

    if query:
        query_lower = query.lower()
        toys = toys.annotate(
            name_lower=Lower('name'),
            desc_lower=Lower('description')
        ).filter(
            Q(name_lower__icontains=query_lower) |
            Q(desc_lower__icontains=query_lower) |
            Q(tags__name__icontains=query_lower)
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



@login_required
def profile_view(request):
    """Личный кабинет пользователя: просмотр и редактирование имени и email."""
    user = request.user

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')

        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email

        user.save()
        messages.success(request, 'Данные профиля обновлены!')
        return redirect('profile')

    return render(request, 'main/profile.html', {'user': user})
