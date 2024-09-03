from fastapi import FastAPI, HTTPException
from api.questions_api import router as questions_router


app = FastAPI()
app.include_router(questions_router)






