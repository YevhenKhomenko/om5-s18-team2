from django.shortcuts import render, HttpResponse, redirect
from .models import Book
from authentication.models import CustomUser
from author.models import Author
from order.models import Order
from .forms import QueryForm, UserForm, BookIDForm, SortFilterForm, EditBookForm
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


def first_view(request):
    form = SortFilterForm(request.GET)
    books = Book.objects.all()
    query_filter = request.GET.get('filter')
    if query_filter:
        to_find = request.GET.get('find')
        if to_find:
            if query_filter == '1':
                books = books.filter(authors__id__contains=to_find)
            elif query_filter == '2':
                books = books.filter(count=int(to_find))
            elif query_filter == '3':
                books = books.filter(name__contains=to_find)
            elif query_filter == '4':
                books = books.filter(description__contains=to_find)
    query_sort = request.GET.get('sort')
    if query_sort:
        if query_sort == '1':
            books = sorted(
                books,
                key=lambda x: x.name, reverse=False
            )
        elif query_sort == '2':
            books = sorted(
                books,
                key=lambda x: x.name, reverse=True
            )
        elif query_sort == '3':
            books = sorted(
                books,
                key=lambda x: x.count, reverse=False
            )
        elif query_sort == '4':
            books = sorted(
                books,
                key=lambda x: x.count, reverse=True
            )

    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'book/main.html', {'page_obj': page_obj, 'form': form})


def by_author(request):
    query = request.GET.get('author_id')
    if query:
        # create a form instance and populate it with data from the request:
        form = QueryForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            author_id = form.cleaned_data['author_id']
            author = Author.get_by_id(author_id)
            if author is None:
                return HttpResponse('There are no such author')
            books = Book.get_by_author(author_id)
            paginator = Paginator(books, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'book/author.html', {'page_obj': page_obj, 'author': author, 'form':form})
        # if a GET (or any other method) we'll create a blank form
    else:
        form = QueryForm()
        books = Book.get_all()
        paginator = Paginator(books, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'book/author.html', {'page_obj': page_obj, 'form':form})


def by_user(request):
    query = request.GET.get('user_id')
    if query:
        # create a form instance and populate it with data from the request:
        form = UserForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            user_id = form.cleaned_data['user_id']
            user = CustomUser.get_by_id(user_id)
            if user is None:
                return HttpResponse('There are no such user')
            books = Order.get_books_by_user(user_id)
            paginator = Paginator(books, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'book/user.html', {'user': user, 'form': form, 'page_obj': page_obj})
        # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()
        books = Book.get_all()
        paginator = Paginator(books, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'book/user.html', {'form': form, 'page_obj': page_obj})


def detail(request, received_id=None):

    if request.method == 'POST':
        form = BookIDForm()
        book = get_object_or_404(Book, id=received_id)
        edit_book_form = EditBookForm(request.POST, instance=book)

        if edit_book_form.is_valid():
            edit_book_form.save()

        return render(request, 'book/detail.html', {'book': book, 'form': form, 'edit_book_form': edit_book_form})

    if request.method == 'GET':
        if received_id:
            form = BookIDForm()
            book = Book.get_by_id(received_id)
            if book is None:
                return HttpResponse('There are no such book')
            initial = {'id': received_id, 'name': book.name, 'description': book.description, 'count': book.count}
            edit_book_form = EditBookForm(initial=initial)
            return render(request, 'book/detail.html', {'book': book, 'form': form, 'edit_book_form': edit_book_form})
        else:
            query = request.GET.get('book_id')
            if query:
                # create a form instance and populate it with data from the request:
                form = BookIDForm(request.GET)
                # check whether it's valid:
                if form.is_valid():
                    # process the data in form.cleaned_data as required
                    book_id = form.cleaned_data['book_id']
                    book = Book.get_by_id(book_id)
                    if book is None:
                        return HttpResponse('There are no such book')
                    initial = {'id': received_id, 'name': book.name, 'description': book.description, 'count': book.count}
                    edit_book_form = EditBookForm(initial=initial)
                    return render(request, 'book/detail.html', {'book': book, 'form': form, 'edit_book_form': edit_book_form})
                # if a GET (or any other method) we'll create a blank form
            else:
                form = BookIDForm()
                edit_book_form = EditBookForm()
                return render(request, 'book/detail.html', {'form': form, 'edit_book_form': edit_book_form})


def unordered(request):
    books = Book.objects.exclude(id__in=[x.book.id for x in Order.objects.all()])
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'book/unordered.html', {'page_obj': page_obj})


def add_book(request):
    if request.method == 'POST':
        form = EditBookForm(request.POST)
        if form.is_valid():
            book = Book.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                count=form.cleaned_data['count']
            )
            book.save()
        return redirect('books')

    else:
        form = EditBookForm()

    return render(request, 'book/add_book.html', {'form': form})


def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('books')




