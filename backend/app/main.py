#
# main.py
#
# @author n1ghts4kura
#

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from router import root_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
