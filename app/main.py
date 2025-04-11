import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

books = [
    {
        'id': 1,
        'title': 'История России',
        'author': 'Гриша',
    },
    {
        'id': 2,
        'title': 'Математика 5 класс',
        'author': 'Елена Владимировна',
    }

]

@app.get('/books', summary='Список книг', tags=['Ручки'])
def read_books():
    return books

@app.get('/books/{book_id}', summary='Книга по id', tags=['Ручки'])
def read_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=404, detail='Книга не найдена')


class Book(BaseModel):
    title: str
    author: str

@app.post('/books', summary='Добавление книги', tags=['Ручки'])
def create_book(book: Book):
    new_book = {
        'id': len(books) + 1,
        'title': book.title,
        'author': book.author,
    }
    books.append(new_book)
    return new_book


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)