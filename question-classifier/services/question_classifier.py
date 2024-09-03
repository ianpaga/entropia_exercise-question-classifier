import re
from config import client

class QuestionClassifier:

    classifier_prompt = """
    As a language model, you are tasked with categorizing questions based on their subject matter. 
    Below is a question that requires classification. Analyze the content and context of the question 
    and determine which of the following categories it best fits: Legal, Accounting, Medical, or Other. 
    If the question does not clearly align with Legal, Accounting, or Medical categories, classify it 
    as Other and provide a brief explanation as to why it does not fit the other categories.

    Question: "{insert_question_here}"

    Please provide the classification and your reasoning for this categorization:

    Classification: 
    Reasoning (if applicable):
    """

    def parse_llm_response(self, classfication_text):
        print(classfication_text)
        match = re.search(r'Classification:\s*(\w+)', classfication_text)
        if match:
            return match.group(1)
        else:
            return "No classification found"


    def classify_question(self, question_text):
        prompt = self.classifier_prompt.format(insert_question_here=question_text)
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
        classification = self.parse_llm_response(llm_response)
        return classification.lower()