from typing import List, Annotated
from fastapi import APIRouter, HTTPException, Query, Body, Path
from app.schemas.book import BookSchema
from data.books import BOOKS

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=List[BookSchema], status_code=200)
async def get_all_books_with_filters(
    category: Annotated[str, Query(description="카테고리로 필터링")] = None,
    author: Annotated[str, Query(description="저자로 필터링")] = None,
    title: Annotated[str, Query(description="제목으로 검색")] = None,
):
    """
    책 목록을 조회합니다.
    필터 조건에 맞는 책들을 반환합니다.
    """
    # 모든 책을 조회하거나 필터링하여 검색
    filtered_books = BOOKS

    if category:
        filtered_books = [
            book
            for book in filtered_books
            if book.get("category").casefold() == category.casefold()
        ]
    if author:
        filtered_books = [
            book
            for book in filtered_books
            if book.get("author").casefold() == author.casefold()
        ]
    if title:
        filtered_books = [
            book
            for book in filtered_books
            if book.get("title").casefold() == title.casefold()
        ]

    return filtered_books


@router.post("", response_model=BookSchema, status_code=201)
async def add_book(
    book_info: Annotated[BookSchema, Body(description="추가할 책 정보")]
):
    """
    새로운 책을 추가합니다.
    성공적으로 생성되면 201 상태 코드와 함께 생성된 책 정보를 반환합니다.
    """
    # 새 책 추가
    for book in BOOKS:
        if book.get("title").casefold() == book_info.title.casefold():
            raise HTTPException(status_code=400, detail="이미 존재하는 책입니다")

    new_book = {
        "title": book_info.title,
        "author": book_info.author,
        "category": book_info.category,
    }
    BOOKS.append(new_book)
    return new_book


@router.put("/{title}", response_model=BookSchema, status_code=200)
async def modify_existing_book(
    book_info: Annotated[BookSchema, Body(description="수정할 책 정보")]
):
    """
    기존 책 정보를 수정합니다.
    성공적으로 수정되면 200 상태 코드와 함께 수정된 책 정보를 반환합니다.
    """
    # 책 정보 수정
    for i, book in enumerate(BOOKS):
        if book.get("title").casefold() == book_info.title.casefold():
            updated_book = book.copy()
            updated_book["author"] = book_info.author
            updated_book["category"] = book_info.category
            BOOKS[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="책을 찾을 수 없습니다")


@router.delete("/{title}", response_model=None, status_code=204)
async def remove_book_by_title(
    title: Annotated[str, Path(description="삭제할 책의 제목")]
):
    """
    책 제목으로 책을 삭제합니다.
    성공적으로 삭제되면 204 상태 코드를 반환합니다.
    """
    for i, book in enumerate(BOOKS):
        if book["title"].casefold() == title.casefold():
            BOOKS.pop(i)
            return
    raise HTTPException(status_code=404, detail=f"Book with title '{title}' not found")
