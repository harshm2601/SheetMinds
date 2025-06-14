import requests
import re
import io
import base64

def extract_python_code(text):
    """
    Extracts the first Python code block from a markdown string.
    """
    match = re.search(r"```python(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # fallback: try to find any code block
    match = re.search(r"```(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def ask_llm(context, error=None, image=None):
    """
    Calls the LLM API (Gemini 2.0 Flash for now) with the user query, schema, sample, and last error if any.
    If image is provided, sends it as a PNG to Gemini for multimodal insights.
    Returns the generated code as a string or insights as text.
    """
    prompt = context.get("prompt")
    if not prompt:
        prompt = f"""
You are a Python data analysis assistant. Given the following context, generate Python code using only pandas, numpy, matplotlib, and seaborn. If a visualization is requested, use matplotlib or seaborn. The dataframe is named 'df'.

IMPORTANT: Only return a single Python code block, no explanations, no markdown, no extra text. The code must use the dataframe 'df' provided in the environment. Do not create or load 'df' yourself.

Context:
Schema: {context['schema']}
Sample Data: {context['sample']}
User Query: {context['query']}
"""
    if error:
        prompt += f"\nLast Error: {error}\nPlease fix the code and try again."
    parts = [{"text": prompt}]
    if image is not None:
        # image should be bytes (PNG)
        b64img = base64.b64encode(image).decode('utf-8')
        parts.append({
            "inline_data": {
                "mime_type": "image/png",
                "data": b64img
            }
        })
    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyCYGDdyoQPKO_seoOObn03PWm9OsEqVDsA",
        json={"contents": [{"parts": parts}]},
        timeout=30
    )
    print(f"LLM response: {response.json()}")
    text = response.json()['candidates'][0]['content']['parts'][0]['text']
    if image is not None:
        return text  # insights
    code = extract_python_code(text)
    return code
