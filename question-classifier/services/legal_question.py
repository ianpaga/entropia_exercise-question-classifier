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


