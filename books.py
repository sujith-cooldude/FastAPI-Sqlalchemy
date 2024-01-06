from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import session
import models
from database import engine, SessionLocal

app = FastAPI()

class Book(BaseModel):
    title:str = Field(min_length=1, max_length=100)
    author:str = Field(min_length=1, max_length=100)
    description:str = Field(min_length=1, max_length=100)
    rating:int = Field(gt=-1, lt=101)

models.Base.metadata.create_all(engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
async def get_books(db:session = Depends(get_db)):
    books = db.query(models.Books).all()
    return books

@app.post("/")
async def create_books(book: Book, db:session = Depends(get_db)):
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

    return book

@app.put("/")
async def update_book(book_id: int, book: Book, db:session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID : {book_id} is not found."
        )
    
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

    return book_model

@app.delete("/")
async def delete_book(book_id: int,db:session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID : {book_id} is not found."
        )

    db.query(models.Books).filter(models.Books.id == book_id).delete()
    db.commit()

    return f"ID: {book_id} deleted Successfully"