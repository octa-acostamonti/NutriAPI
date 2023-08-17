from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None




@app.get("/")
async def root():
    return  ({"mi no bia":"e e e "})


@app.get("/proteinas/")
def get_proteinas():
    return {"manzana":"20gr"}

@app.post("/createposts/")
def create_posts(new_post: Post):
    print(new_post)
    print({"new_post":f"title: {new_post.title} content: {new_post.content}"})
    return {"new_post":f"title: {new_post.title} content: {new_post.content}"}
# title str, content str
