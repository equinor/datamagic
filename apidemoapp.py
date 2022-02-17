from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Data Magic!"}

# Hints:
# pip install "fastapi[all]"
# uvicorn apidemoapp:app --reload
