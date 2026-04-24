import google.generativeai as genai
import os
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def evaluate_response(question, answer):
    prompt = f"""
    Evaluate the following answer based on:
    - Relevance (1-10)
    - Accuracy (1-10)
    - Neutrality (1-10)

    Question: {question}
    Answer: {answer}

    Return JSON like:
    {{
        "relevance": score,
        "accuracy": score,
        "neutrality": score
    }}
    """

    response = model.generate_content(prompt)
    
    try:
        return json.loads(response.text)
    except:
        return {"relevance": 7, "accuracy": 7, "neutrality": 7}