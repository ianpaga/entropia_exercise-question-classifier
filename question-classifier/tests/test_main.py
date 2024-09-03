from fastapi.testclient import TestClient
from main import app
from services.question_classifier import QuestionClassifier


client = TestClient(app)

def test_legal_question():
    question = client.post("/ask/", json={"text": "What are the legal implications of a contract?"})
    category = QuestionClassifier().classify_question(question.text)
    assert question.status_code == 200
    assert question.json()["category"] == "legal"

def test_medical_question():
    question = client.post("/ask/", json={"text": "What dietary changes can help with high cholesterol?"})
    category = QuestionClassifier().classify_question(question.text)
    assert question.status_code == 200
    assert question.json()["category"] == "medical"

def test_accounting_question():
    question = client.post("/ask/", json={"text": "How should I record revenue from a long-term contract?"})
    category = QuestionClassifier().classify_question(question.text)
    assert question.status_code == 200
    assert question.json()["category"] == "accounting"

