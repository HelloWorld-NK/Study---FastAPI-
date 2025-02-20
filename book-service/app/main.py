from fastapi import FastAPI

# from .api.book import router  # 기존 코드 주석 처리
from .books_2 import app as router  # 새로운 코드 추가

app = FastAPI(title="Book Service")

app.include_router(router)
