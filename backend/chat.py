from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from agent import send_book_details_to_letta
from api import FetchBooks
from config import settings

router = APIRouter()

# Schemas
class DescRequest(BaseModel):
    isbn13: str

class GetDesc(BaseModel):
    title: str
    authors: str
    isbn13: str
    description: str
    cover: str

class LettaRes(BaseModel):
    url: str


@router.post("/chat", response_model=LettaRes)
async def get_url_from_letta(request: DescRequest):
    try:
        books = FetchBooks(auth_key=settings.AUTH_KEY)
        desc_list = books.get_description(request.isbn13)
        if not desc_list:
            raise HTTPException(status_code=404, detail="Description not found")
        desc_obj = desc_list

        desc = (
            f"Title: {desc_obj.get('title','')}\n"
            f"Authors: {desc_obj.get('authors','')}\n"
            f"ISBN13: {desc_obj.get('isbn13','')}\n"
            f"Description: {desc_obj.get('description','')}\n"
            f"Cover: {desc_obj.get('cover','')}"
        ).strip()

        url = send_book_details_to_letta(desc)
        if not isinstance(url, str) or not url:
            raise HTTPException(status_code=502, detail="Agent did not return a URL")

        return LettaRes(url=url)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
