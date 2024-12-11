import google.generativeai as genai
from decouple import config

gemini_key = config("GEMINI_API_KEY")
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_ai_res(input_text):
    try:
        response = model.generate_content(input_text)
        return response
    except Exception as e:
        return f"Ai resposnce could not be generated due to error:- {str(e)}"