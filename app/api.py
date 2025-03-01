from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(
        title="RodFaiBob-Backend",
        description="AI",
        version="1.0.0",
    )

    return app

app = create_app()

@app.get("/")
async def read_root():
    return {"message": "Welcome to RodFaiBob-Backend"}