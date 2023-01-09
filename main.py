from fastapi import FastAPI

from game_core_server.controller import search_controller


app = FastAPI()

app.include_router(search_controller.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
