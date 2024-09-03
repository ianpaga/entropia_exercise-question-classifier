from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from fastapi import APIRouter
from validator import Question
from services.question_classifier import QuestionClassifier
from services.question_factory import QuestionFactory

""" 
This file defines the specific behavior for the /ask/ route, handling 
the logic for classifying questions and generating responses.
@router.post("/ask/"): This decorator defines a route at /ask/ that accepts POST requests. 
When a POST request is sent to /ask/, the ask_question function is executed.
(async: prevents blocking operations and allows the server to handle multiple requests concurrently)
"""

router = APIRouter()

@router.post("/ask/")
async def ask_question(question: Question):
    category = QuestionClassifier().classify_question(question.text)
    #print(category)
    #import pdb;pdb.set_trace()
    if category == "other":
        raise HTTPException(status_code=400, detail="The question cannot be classified.")
    
    # `question_class` is the instance of the  question class 
    # (based on the category) and generates an answer using an LLM
    question_class = QuestionFactory.get_question(category)
    answer = question_class.ask(question_text=question.text)
    return {"category": category, "answer": answer}