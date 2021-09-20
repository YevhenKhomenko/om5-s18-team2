import os
import pandas as pd
import  numpy as np
import datetime
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'library.settings')

import django
django.setup()

from authentication.models import CustomUser
from author.models import Author
from book.models import Book
from order.models import Order
from django.utils import timezone
AUTHORS = pd.read_excel('authors.xlsx', index_col=0)


BOOKS = pd.read_excel('books.xlsx', index_col=0)

USERS = [['john_doe@gmail.com', 'ololo', 'John', 'DJ', 'Doe'],
         ['glenn_wise@gmail.com', 'ololo', 'Glenn', 'WS', 'Wise'],
         ['derec_getter@gmail.com', 'abbba', 'Derec', 'DC', 'Getter'],
         ['john_lennon@gmail.com', 'ololo', 'John', 'DJ', 'Lennon'],
         ['johan_getsby@yahoo.com', 'abba', 'Johan', 'DG', 'Getsby'],
         ['kate_perry@yahoo.com', 'abba', 'Kate', 'KP', 'Perry'],
         ['mary_kay@yahoo.com', 'abba', 'Mary', 'MK', 'Kay'],
         ['gloria_roy@gmail.com', 'reggy', 'Gloria', 'GR', 'Roy'],
         ['anny_smith@gmail.com', 'reggy', 'Anny', 'AS', 'Smith'],
         ['julia_desmond@gmail.com', 'abba', 'Julia', 'JD', 'Desmond'],
         ['susie_roy@gmail.com', 'reggy', 'Susie', 'SR', 'Roy']]

data = np.random.randint(1,10,size=200)
ORDERS = pd.DataFrame(data, columns=['author'])
data2 = np.random.randint(1,136,size=200)
ORDERS['books'] = data2


def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.
    for y in BOOKS.itertuples():
        try:
            obj = Book.objects.get(name=y[1], description=y[2],
                                     count=y[3])
        except Book.DoesNotExist:
            Book.create(name=y[1], description=y[2],
                                     count=y[3])
    for x in AUTHORS.itertuples():
        try:
            obj = Author.objects.get(name=x[1], surname=x[2],
                                     patronymic=x[3])
        except Author.DoesNotExist:
            Author.create(name=x[1], surname=x[2],
                                     patronymic=x[3])

    for elem in AUTHORS.itertuples():
        obj = Author.objects.get(name=elem[1], surname=elem[2],
                                     patronymic=elem[3])
        for book in BOOKS.itertuples():
            if book[4] == elem[0]:
                obj.books.add(Book.objects.get(name=book[1], description=book[2],
                                     count=book[3]))

    for user in USERS:
        try:
            obj = CustomUser.objects.get(email = user[0], password = user[1], first_name=user[2],
                          middle_name=user[3], last_name=user[4])
        except CustomUser.DoesNotExist:
            CustomUser.create(email = user[0], password = user[1], first_name=user[2],
                          middle_name=user[3], last_name=user[4])

    for order in ORDERS.itertuples():
        counter_user = order[1]
        counter_book = order[2]
        user = CustomUser.objects.get(email = USERS[counter_user][0])
        book = Book.objects.get(name=BOOKS.iloc[counter_book]['Name'],
                                description=BOOKS.iloc[counter_book]['Description'],
                                     count=BOOKS.iloc[counter_book]['Count'])
        try:
            obj = Order.objects.get(user = user, book=book)
        except Order.DoesNotExist:
            Order.create(user = user, book=book,
                         plated_end_at = timezone.now() - datetime.timedelta(days=random.randint(-10, 10)))


# Start execution here!
if __name__ == '__main__':
    print("Starting population script...")
    populate()