from config import client
from services.question import Question


class AccountingQuestion(Question):

    prompt = """
    You are an expert accountant with extensive knowledge in financial accounting, tax laws, 
    and corporate finance. Your expertise includes but is not limited to bookkeeping, financial 
    reporting, auditing, tax preparation, and financial planning. Please provide detailed, 
    accurate, and professional answers to the user's question: "{insert_question_here}".
    Act as their personal accountant.
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
