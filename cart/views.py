from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import Toy
from .models import CartItem
from main.models import Purchase
from django.utils import timezone


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.toy.price * item.quantity for item in cart_items)

    # обработка изменения количества
    if request.method == 'POST':
        for item in cart_items:
            new_quantity = request.POST.get(f'quantity_{item.id}')
            if new_quantity:
                new_quantity = int(new_quantity)
                if new_quantity <= 0:
                    item.delete()
                else:
                    item.quantity = new_quantity
                    item.save()
        return redirect('cart')

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


@login_required
def add_to_cart(request, toy_id):
    toy = get_object_or_404(Toy, id=toy_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, toy=toy)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.info(request, f"Товар '{toy.name}' добавлен в корзину 🛒")
    return redirect('home')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.warning(request, f"Товар '{item.toy.name}' удалён из корзины ❌")
    return redirect('cart')


@login_required
def checkout_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart')

    for item in cart_items:
        Purchase.objects.create(
            user=request.user,
            toy=item.toy,
            quantity=item.quantity,
            price=item.toy.price
        )

    cart_items.delete()

    messages.success(request, 'Покупка успешно завершена!')
    return redirect('profile')

