from django.shortcuts import render, redirect, get_object_or_404

from .models import *
from .forms import CustomUserForm
from django.views.generic import DeleteView

from rest_framework import generics
from .serializers import UserListSerializer, UserDetailSerializer


def index(request):
    users = CustomUser.objects.order_by('last_name')
    return render(
        request,
        'authentication/index.html',
        {'title': 'Посетители Библиотеки', 'users': users}
    )


def detail(request, user_id):
    user = CustomUser.get_by_id(user_id)
    context = {
        'title': f'Пользователь номер: {user.id}',
        'user': user
    }

    return render(
        request,
        'authentication/detail.html',
        context
    )


def create(request):
    error = ""
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            error = "неверная форма"

    data = {
        'form': CustomUserForm(),
        'error': error
    }
    return render(request, 'authentication/create.html', data)


def edit(request, user_id):
    error = ""

    if request.method == "POST":
        user = CustomUser.objects.get(pk=user_id)
        user_updated = CustomUserForm(request.POST, instance=user)
        if user_updated.is_valid():
            user_updated.save()
            return redirect("/")
        else:
            error = "Некорректные данные"

    user = CustomUser.objects.get(pk=user_id)

    data = {
        'form': CustomUserForm(instance=user),
        'error': error
    }
    return render(request, 'authentication/edit.html', data)


def delete_user(request, user_id=0):
    if request.method == "POST" and user_id != 0:
        CustomUser.delete_by_id(user_id)
        return redirect("/")


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = CustomUser.get_all()


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer

    def get_object(self):
        return get_object_or_404(CustomUser, pk=self.kwargs.get('user_id'))


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserDetailSerializer
