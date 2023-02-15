
#тут будет Фастапи

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/", response_class=FileResponse)
def read_root():
    return "public/index.html"


