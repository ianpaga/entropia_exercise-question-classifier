from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from fastapi import APIRouter
from validator import Question
from services.question_classifier import QuestionClassifier
from services.question_factory import QuestionFactory

router = APIRouter()

@router.post("/ask/")
async def ask_question(question: Question):
    category = QuestionClassifier().classify_question(question.text)
    #print(category)
    #import pdb;pdb.set_trace()
    if category == "other":
        raise HTTPException(status_code=400, detail="The question cannot be classified.")
    
    question_class = QuestionFactory.get_question(category)
    answer = question_class.ask(question_text=question.text)
    return {"category": category, "answer": answer}