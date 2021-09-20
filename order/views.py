from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from .forms import EditOrderForm
from authentication.models import CustomUser
from django.core.paginator import Paginator
from django.utils import timezone


def first_view(request):
    orders = sorted(
        Order.get_all(),
        key=lambda x: x.plated_end_at, reverse=True
    )
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'order/orders.html', {'page_obj': page_obj})


def bad_users(request):
    users = list(set([x.user for x in Order.objects.filter(plated_end_at__lte=timezone.now())]))
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'order/bad_users.html', {'page_obj': page_obj})


def order_details(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        form = EditOrderForm(request.POST, instance=order)

        if form.is_valid():
            form.save()

        return render(request, 'order/order_details.html', {'order': order, 'form': form})

    if request.method == 'GET':
        order = get_object_or_404(Order, id=order_id)
        form = EditOrderForm(request.GET, instance=order)
        return render(request, 'order/order_details.html', {'order': order, 'form': form})


def create_order(request):
    if request.method == 'POST':
        form = EditOrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=form.cleaned_data['user'],
                book=form.cleaned_data['book'],
                end_at=form.cleaned_data['end_at'],
                plated_end_at=form.cleaned_data['plated_end_at']
            )
            order.save()
        return redirect('books')

    else:
        form = EditOrderForm()

    return render(request, 'order/create_order.html', {'form': form})


def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('orders')
