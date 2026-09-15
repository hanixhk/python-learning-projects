from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def read_root():
    return {
    "message": "Personal Transaction API is running"
    }

@app.get("/hello/{name}")
def read_name(name: str):
    return {"Hello": name}

@app.get("/products")
def read_products(category: str):
    return {"category": category}