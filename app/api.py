from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.search.search_api import router as search_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="RodFaiBob-Backend",
        description="AI",
        version="1.0.0",
    )

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Change this to specific origins for security
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )

    return app

app = create_app()

app.include_router(search_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to RodFaiBob-Backend"}

#! /usr/bin/env python3
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
