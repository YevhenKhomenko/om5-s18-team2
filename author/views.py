from django.shortcuts import render, redirect
from .models import Author
from book.models import Book
from .forms import AuthorForm
from rest_framework import generics
from .serializers import AuthorDetailSerializer, AuthorListSerializer, AuthorSerializer
from django.shortcuts import get_object_or_404


def index(request):
    authors = Author.objects.order_by('-id')
    return render(
        request,
        'author/index.html',
        {'title': 'Авторы', 'authors': authors}
    )


def detail(request, author_id):
    author = Author.get_by_id(author_id)
    books = Book.objects.filter(authors__id=author_id)
    context = {
        'title': f'{author.get_full_name()}',
        'author': author,
        'books': books
    }
    return render(
        request,
        'author/detail.html',
        context
    )


def add_author(request, author_id=0):
    if request.method == 'GET':
        if author_id == 0:
            form = AuthorForm()
        else:
            author = Author.objects.get(pk=author_id)
            form = AuthorForm(instance=author)
        return render(request, 'author/add_author.html', {'form': form})
    else:
        if author_id == 0:
            form = AuthorForm(request.POST)
        else:
            author = Author.objects.get(pk=author_id)
            form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
    return redirect('authors')


def del_author(request, author_id):
    author = Author.objects.get(pk=author_id)
    author.delete()
    return redirect('authors')


class AuthorListAPIView(generics.ListAPIView):
    queryset = Author.get_all()
    serializer_class = AuthorListSerializer


class AuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorDetailSerializer

    def get_object(self):
        return get_object_or_404(Author, pk=self.kwargs.get('author_id'))

class AuthorCreateAPIView(generics.CreateAPIView):
    serializer_class = AuthorDetailSerializer
