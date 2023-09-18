from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import base, engine
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router
from templates.index import index

app = FastAPI()
app.title = "FastAPI CRUD - Movies"
app.version = "0.0.2"
app.description = "This is a simple CRUD API application made with FastAPI"
app.docs_url = "/docs"

app.add_middleware(ErrorHandler)
app.include_router(movie_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")

base.metadata.create_all(bind=engine)

# --------------------------------------------------------------------------------


@app.get("/", tags=["Home"])
def welcome() -> HTMLResponse:
    page: str = index
    return HTMLResponse(content=page, status_code=200)


# --------------------------------------------------------------------------------
# To run the server, try to use the following command:
# uvicorn main:app --reload --port 5000 --host 0.0.0.0
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=5000)
