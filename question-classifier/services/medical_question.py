from config import client
from services.question import Question


class MedicalQuestion(Question):

    prompt = """
    Imagine you are an expert medical doctor with extensive knowledge and experience 
    in various fields of medicine. A patient has come to you with a question regarding 
    their health: "{insert_question_here}". Please provide a detailed, informative, 
    and empathetic response to the patient's inquiry, drawing upon your medical expertise.
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



