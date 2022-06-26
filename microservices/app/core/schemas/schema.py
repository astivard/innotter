from typing import List
from pydantic import BaseModel


class Post(BaseModel):
    id: int
    likes: int


class Page(BaseModel):
    id: int
    name: str
    all_posts: int
    all_likes: int
    subscribers: int
    posts: List[Post]


class Statistics(BaseModel):
    username: str
    pages: List[Page]

