import os
import json

from uuid import uuid4
from mangum import Mangum
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from typing import Literal, Optional


app = FastAPI()


class Book(BaseModel):
    name: str
    price: float
    genre: Literal['fiction', 'non-fiction']
    book_id: Optional[str] = uuid4().hex


BOOKS = []
BOOKS_FILE = 'books.json'

if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, 'r') as f:
        BOOKS = json.load(f)


@app.get('/')
def read_root():
    return {'message': 'Hello World'}


@app.get('/list-books')
async def list_books():
    return {'books': BOOKS}


@app.post('/add-book')
async def add_book(book: Book):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    BOOKS.append(json_book)

    with open(BOOKS_FILE, 'w') as f:
        json.dump(BOOKS, f)

    return {'book_id': book.book_id}


handler = Mangum(app=app)
