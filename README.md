
# Dockerized FastAPI Server for LLM-Based Question Classification and Answering 🤖 

## Project Overview

This project is a Dockerized FastAPI server designed to classify and answer questions using a large language model (LLM). The server processes input questions, classifies them into one of the following categories: "legal", "accounting" or "medical" (raising HTTPException if category = "other"). Once it has classified the user's question, the LLM generates an appropriate response based on predefined prompts for each category. 

For example: If the category the quesiton is "What are the legal implications of not paying medical bills?", the category is "legal", and the LLM will generate a response acting as your a lawyer with expertise in intellectual property, criminal defense, contract law, etc. See below for a detailed question-response example. 

### Key Features:
- **Question Classification:** The server categorizes questions into specific types ("legal", "accounting", "medical") using an LLM.
- **Tailored Responses:** Depending on the classification, the server generates answers with prompts tailored to the question type. If "legal", the LLM will act as your lawyer, for example.
- **Dockerized for Easy Deployment:** The entire application is containerized using Docker, ensuring easy deployment and portability.

### Input and Output:
- **Input:** A JSON object with a field `text` containing the question.
- **Output:** A JSON response with the `category` of the question and the generated `answer`.

### Example of Input and Output:

- **Input:** A JSON object containing a question send to endpoint /ask/ (using [POSTMAN](https://www.postman.com/)):
```
{
  "text": "What are the legal implications of not paying medical bills?"
}
```

- **Output:** A JSON response with the `category` and `answer` (only part of the reponse shown here for clarity)

```
{
    "category": "legal",
    "answer": "I'd be happy to advise on the legal implications of not paying medical bills.\n\n**Background and Primary Concerns**\n\nWhen a client fails to pay medical bills, they may face a range of legal, financial, and personal consequences. As an attorney, it's essential to understand the underlying factors that led to this situation and the client's primary concerns. Are they struggling to pay due to financial hardship, insurance issues, or other medical emergencies? Understanding the root cause will help guide our response.\n\n**Legal Implications and Consequences**\n\nFailing to pay medical bills can lead to various legal consequences, depending on the jurisdiction and specific circumstances. Here are some potential legal implications to consider:\n\n1. **Bad Debt Reporting**: Credit reporting agencies may report outstanding medical debts to the client's credit report, significantly impacting their credit score.\n2. **Debt Collection Complaints**: Medical providers or collection agencies can file debt collection complaints with the court, seeking judgment and potentially leading to wage garnishment, property liens, or even lawsuits.\n3. **collections lawsuits**: If a debt collection agency prevails in a lawsuit, they may obtain a court judgment, which can lead to a lien on the client's property, including real estate, personal assets, or future earnings.\n4. **Wage Garnishment**: A court judgment can result in the garnishment of the client's wages, with up to 25% of their income being withheld to satisfy the debt."
}
```

## Project Structure

### 1. `main.py`
This is the entry point for the [FastAPI](https://fastapi.tiangolo.com/) application.

```python
from fastapi import FastAPI
from api.questions_api import router as questions_router

app = FastAPI()
app.include_router(questions_router)
```
- **Example:** This script initializes the FastAPI app and includes the question handling router.

### 2. `config.py`
Handles the configuration for the API client, specifically for the [Groq API](https://console.groq.com/keys).

```python
import os
from groq import Groq

GROQ_API_KEY = os.getenv('GROQ_API_KEY', None)

if not GROQ_API_KEY:
    raise ValueError('API KEY NOT FOUND!')

client = Groq(api_key=GROQ_API_KEY)
```
- **Example:** Loads the API key from the environment and initializes the Groq client.

### 3. `validator.py`
Defines the data model for validating incoming questions using Pydantic.

```python
from pydantic import BaseModel

class Question(BaseModel):
    text: str
```
- **Example:** Ensures that the input question has the correct structure, raising an error if it does not.

### 4. `requirements.txt`
Lists all the Python dependencies needed to run the application.

```text
fastapi==0.112.2
groq==0.10.0
pydantic==2.8.2
uvicorn==0.30.6
pytest==8.3.2
```
- **Example:** Specifies the versions of FastAPI, Groq, and other dependencies.

### 5. `Dockerfile`
Defines the Docker image for the application.

```Dockerfile
FROM python:3.9

RUN mkdir -p /app
ENV APP_HOME=/app
WORKDIR $APP_HOME

COPY . $APP_HOME/
RUN pip3 install --no-cache-dir -r $APP_HOME/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
- **Example:** Sets up a Python 3.9 environment, installs dependencies, and runs the FastAPI server.

### 6. `docker_build_run.sh`
Shell script for building and running the Docker container.

```bash
#!/usr/bin/env bash

docker rm -f llm_app
set -x

docker build . --platform linux/amd64 -f Dockerfile -t llm_app:latest
docker run -d --restart unless-stopped -e GROQ_API_KEY -p 8000:8000 llm_app
```
- **Example:** Automates the Docker build and run process. Simply run ./docker_build_run.sh for creating the Docker image and container.

### 7. `api/questions_api.py`
Handles the routing and logic for processing questions.

```python
from fastapi import APIRouter, HTTPException
from validator import Question
from services.question_classifier import QuestionClassifier
from services.question_factory import QuestionFactory

router = APIRouter()

@router.post("/ask/")
async def ask_question(question: Question):
    category = QuestionClassifier().classify_question(question.text)
    if category == "other":
        raise HTTPException(status_code=400, detail="The question cannot be classified.")
    
    question_class = QuestionFactory.get_question(category)
    answer = question_class.ask(question_text=question.text)
    return {"category": category, "answer": answer}
```
- **Example:** Routes incoming questions, classifies them, and returns a generated answer.

### 8. `services/question_classifier.py`
Implements the logic to classify questions using an LLM.

```python
import re
from config import client

class QuestionClassifier:
    classifier_prompt = """
    As a language model, you are tasked with categorizing questions based on their subject matter.
    ...
    Classification: 
    Reasoning (if applicable):
    """
    def parse_llm_response(self, classification_text):
        match = re.search(r'Classification:\s*(\w+)', classification_text)
        return match.group(1) if match else "No classification found"

    def classify_question(self, question_text):
        prompt = self.classifier_prompt.format(insert_question_here=question_text)
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        llm_response = response.choices[0].message.content
        return self.parse_llm_response(llm_response).lower()
```
- **Example:** Classifies questions into categories like legal, accounting, or medical. It also add its reasoning for asigning that category. Notice that we implement the `model=llama3-8b-8192` but this can be changed according to project's needs.

### 9. `services/question_factory.py`
Provides the appropriate question handler based on the classification.

```python
from services.legal_question import LegalQuestion
from services.accountant_question import AccountingQuestion
from services.medical_question import MedicalQuestion

class QuestionFactory:
    @staticmethod
    def get_question(question_type):
        if question_type == 'legal':
            return LegalQuestion()
        elif question_type == 'accounting':
            return AccountingQuestion()
        elif question_type == 'medical':
            return MedicalQuestion()
        else:
            return OtherQuestion()
```
- **Example:** Returns a specific handler object based on the question type. This is good if the project grows as it modularizes our code; we can easily implement more categories or cases.

### 10. `services/question.py`
Abstract base class for different types of questions.

```python
from abc import ABC, abstractmethod

class Question(ABC):
    @abstractmethod
    def ask(self, question_text):
        pass
```
- **Example:** The Question class is designed to be a base class for different types of question classes, like `LegalQuestion`, `MedicalQuestion` and `AccountingQuestion`. Each subclass will inherit from Question (`LegalQuestion(Question)`) and must provide an implementation for the ask method. By defining ask as an abstract method, python ensures that any subclass of Question cannot be instantiated unless it implements the ask method.

### 11. `services/legal_question.py`

```python
from config import client
from services.question import Question


class LegalQuestion(Question):

    prompt = """
    Imagine you are a seasoned lawyer with expertise in intellectual property, criminal defense, 
    contract law, etc. A client has approached you with the following question: "{insert_question_here}". 
    Please provide a detailed, legally-informed response that addresses the client's concerns 
    and outlines potential legal strategies or considerations.
    """


    def ask(self, question_text):
        prompt = self.prompt.format(insert_question_here=question_text)
        response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        llm_response = response.choices[0].message.content
        return llm_response
```
The LegalQuestion class is a subclass of the abstract Question class, designed to handle legal queries. It uses a predefined prompt to simulate a conversation with a lawyer and generates responses using an LLM. 

<!-- The `ask` method:
1. Formats the prompt by inserting the user's question.
2. Sends the formatted prompt to an LLM (using the client.chat.completions.create method).
3. Extracts the response content from the LLM's output.
4. Returns the generated legal advice. -->

In `/api/questions_api.py` (snippet)

```python
question_class = QuestionFactory.get_question(category)
    answer = question_class.ask(question_text=question.text)
    return {"category": category, "answer": answer}
```

the `question_class` can be either the classes `LegalQuestion()` (if category='legal'), `MedicalQuestion()` (if category='medical'), or `AccountingQuestion()` (if category='accounting'). Then, the question is asked, and the corresponding answer is generated.



### 12. `tests/test_main.py`
Contains unit tests for verifying the functionality of the server. We set up a few questions to which we know their category.

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_legal_question():
    response = client.post("/ask/", json={"text": "What are the legal implications of a contract?"})
    assert response.status_code == 200
    assert response.json()["category"] == "legal"

def test_medical_question():
    response = client.post("/ask/", json={"text": "What dietary changes can help with high cholesterol?"})
    assert response.status_code == 200
    assert response.json()["category"] == "medical"

def test_accounting_question():
    response = client.post("/ask/", json={"text": "How should I record revenue from a long-term contract?"})
    assert response.status_code == 200
    assert response.json()["category"] == "accounting"
```
- **Example:** Tests various types of questions to ensure they are classified and handled correctly. To run this tests, `cd tests/`, and then run `pytest .` or `pytest test_main.py`. The output should look like this:

```bash
collected 3 items                                                                                   
test_main.py ...                                                                                                            
===================== 3 passed in 7.87s ===================== [100%]
```

## Building and Running the Docker Image

To build and run the Docker container for this project, follow these steps:

### 1. Export Key

- Export groq key before building the Docker image. Run on terminal:

```bash
export GROQ_API_KEY = ‘YOUR_GROQ_KEY_1234567’
```

If the key is not exported the following error will be raised by `config.py`:

```bash
raise ValueError('API KEY NOT FOUND!')
ValueError: API KEY NOT FOUND!
```

- Check if the key has be correctly exported 

```bash
$GROQ_API_KEY
```
Your key should be printed on the terminal. Now you can build and run docker.

### 2. **Build the Docker Image:**
   ```bash
   ./docker_build_run.sh
   ```
   This script will build the Docker image and run the container.


   ```bash
   #!/usr/bin/env bash

    docker rm -f llm_app
    set -x

    docker build . --platform linux/amd64 -f Dockerfile -t llm_app:latest

    docker run -d --restart unless-stopped -e GROQ_API_KEY -p 8000:8000 llm_app
   ```
   Last command runs the container in detached mode (freeing the terminal), with the server listening on port 8000.

### 3. Check status and send messege to endpoint /ask/

- You can check the status of your container:

```bash
docker ps -a
```

Or one can go to the Docker app, click on the container and see the Logs, which should look something like this:

```bash
2024-09-03 10:57:35 INFO:     Started server process [1]
2024-09-03 10:57:35 INFO:     Waiting for application startup.
2024-09-03 10:57:35 INFO:     Application startup complete.
2024-09-03 10:57:35 INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

- Send a message with POST to http://localhost:8000/ask/ : 

```bash
{
  "text": "What are the legal implications of not paying medical bills?"
}
```
click SEND in POSTMAN and see the output:

```bash
{
    "category": "legal",
    "answer": "As a seasoned lawyer with experience in multiple areas of law, including intellectual property, criminal defense, and contract law, I would provide the following detailed and legally-informed response to address the client's concerns regarding the legal implications of not paying medical bills. […]”
}
```

## Summary

The FastAPI server in this project can classify and respond to questions provided using a LLM. It's fully Dockerized for easy deployment, and suitable for a production environment.
