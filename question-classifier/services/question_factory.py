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
