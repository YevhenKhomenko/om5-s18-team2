import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
r = requests.get('https://www.oclc.org/en/worldcat/library100/top500.html')
print(r.status_code)
books = pd.DataFrame(columns=['Name', 'Description', 'Count', 'Author'])
print(books)
authors = pd.DataFrame(columns=['Name', 'Surname', 'Patronymic', 'Fullname'])
soup = BeautifulSoup(r.content, 'html.parser')
p2 = soup.find_all('tr')
for i in p2[1:150]:
    tds = i.find_all('td')
    if tds:
        link = tds[1].a.get('href')
        book = requests.get(link)
        b_soup = BeautifulSoup(book.content, 'html.parser')
        desc = b_soup.find('div', id="summary")
        if desc:
            text = tds[2].text
            if authors.loc[authors['Fullname'].isin([text])].empty:
                words = text.split()
                if len(words) > 2:
                    authors.loc[authors.shape[0]] = [words[0], words[1], words[2], text]
                elif len(words) == 2:
                    authors.loc[authors.shape[0]] = [words[0], words[0][0] + words[1][0], words[1], text]
                else:
                    authors.loc[authors.shape[0]] = [words[0], words[0], words[0], text]
            author_index = authors.loc[authors['Fullname'] == text].index[0]
            print(author_index)
            books.loc[books.shape[0]] = [tds[1].text, desc.text, random.randint(2, 10), author_index]
            print(desc.text.strip())
            print('book ' + tds[1].text + ' author ' + tds[2].text)

books.to_excel("books.xlsx", sheet_name="Books")
authors.to_excel("authors.xlsx", sheet_name="Authors")
