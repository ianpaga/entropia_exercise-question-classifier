import os
from groq import Groq

GROQ_API_KEY = os.getenv('GROQ_API_KEY', None)
#print(GROQ_API_KEY)

if not GROQ_API_KEY:
    raise ValueError('API KEY NOT FOUND!')

client = Groq(
    api_key=GROQ_API_KEY
)
