from fastapi import FastAPI
from app.search.search_api import router as search_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="RodFaiBob-Backend",
        description="AI",
        version="1.0.0",
    )

    return app

app = create_app()

app.include_router(search_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to RodFaiBob-Backend"}