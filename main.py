from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from config.database import base, engine
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router

from utils.jwt_manager import create_token
from dotenv import load_dotenv

import os

app = FastAPI()
app.title = "FastAPI CRUD - Movies"
app.version = "0.0.2"
app.description = "This is a simple CRUD API application made with FastAPI"
app.docs_url = "/docs"

app.add_middleware(ErrorHandler)
app.include_router(movie_router, prefix="/api/v1")

base.metadata.create_all(bind=engine)

# Load environment variables from .env file
load_dotenv()

# --------------------------------------------------------------------------------


class User(BaseModel):
    email: str = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=5, max_length=50)


# --------------------------------------------------------------------------------


@app.get("/", tags=["Home"])
def welcome() -> HTMLResponse:
    page: str = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* Insert your CSS styles here */
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        
        header, main, footer {
            padding: 20px;
        }
        
        header {
            background-color: #333;
            color: #fff;
            text-align: center;
        }
        
        main {
            flex: 1;
            max-width: 800px;
            margin: 0 auto;
        }
        
        a {
            color: #007bff;
            text-decoration: none;
        }
        
        footer {
            background-color: #333;
            color: #fff;
            text-align: center;
            padding: 10px 0;
            position: absolute;
            bottom: 0;
            width: 100%;
        }
    </style>
    <title>Movie API Documentation</title>
</head>
<body>
    <header>
        <h1>Welcome to Movie API Documentation</h1>
    </header>
    <main>
        <section>
            <h2>Using the Movie API</h2>
            <p>This API allows you to perform CRUD operations on movie data.</p>
            <h3>API Base URL:</h3>
            <p>http://localhost:5000</p>
        </section>
        <section>
            <h2>Accessing API Documentation</h2>
            <p>To access the API documentation and test endpoints, go to:</p>
            <p><a href="/docs" target="_blank">Swagger Documentation</a></p>
        </section>
    </main>
    <footer>
        <p>&copy; 2023 Movie API</p>
    </footer>
</body>
</html>
"""

    return HTMLResponse(page, status_code=200)


# --------------------------------------------------------------------------------


@app.post("/login", tags=["login"])
def login(user: User):
    if user.email == "test@gmail.com" and user.password == "demokeys12345":
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Login successful",
                "token": create_token(user.dict(), os.getenv("KEY")),
            },
        )
    raise HTTPException(status_code=401, detail="Invalid credentials")


# --------------------------------------------------------------------------------
# To run the server, try to use the following command:
# uvicorn main:app --reload --port 5000 --host 0.0.0.0
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=5000, reload=True)
