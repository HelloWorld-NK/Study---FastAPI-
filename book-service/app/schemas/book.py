from pydantic import BaseModel, Field


class BookSchema(BaseModel):
    """기본 책 정보를 정의하는 베이스 스키마"""

    title: str = Field(..., min_length=1, description="책 제목")
    author: str = Field(..., min_length=1, description="저자 이름")
    category: str = Field(..., min_length=1, description="책 카테고리")
