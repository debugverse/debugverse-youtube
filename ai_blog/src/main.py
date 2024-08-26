from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from app.db import db
from app.creator import create_blogpost
from app.models import RequestModel, BlogPost
from pydantic import ValidationError
from typing import List
from fastapi.templating import Jinja2Templates

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/generate_post")
async def hello(req: RequestModel):
    result, response = await create_blogpost(req.topic)

    if not result:
        return JSONResponse(status_code=500, content={"error": "could not generate post"})

    try:
        post = BlogPost(**response)
    except ValidationError:
        return JSONResponse(status_code=500, content={"error": "Could not parse post"})

    dbresult = await db.add_post(post)

    if not dbresult:
        return JSONResponse(status_code=500, content={"error": "Could not save post"})

    return JSONResponse(status_code=200, content={"message": "Post saved successfully."})


@app.get("/list_posts", response_model=List[BlogPost])
async def list_posts(request: Request):
    posts = await db.list_posts()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
