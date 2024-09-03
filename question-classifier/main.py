from fastapi import FastAPI
from api.questions_api import router as questions_router

"""
This file sets up the FastAPI application and tells it to use the routes defined in questions_api.py
"""

app = FastAPI() # FastAPI application instance
app.include_router(questions_router) # it connects the routes in questions_api.py to the main app






