import os
import httpx

def ask_gpt(instruction, question):
    """Send a minimal request to OpenAI GPT-4o Mini."""
    headers = {"Authorization": f"Bearer eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIxZjEwMDQ5MTNAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.nbT1BzKJ4xz_LZM8jo4l_6957hbgC8cNHQHp0vLuZFc", "Content-Type": "application/json"}
    payload = {"model": "gpt-4o-mini", "messages": [{"role": "system", "content": instruction}, {"role": "user", "content": question}], "temperature": 0}
    
    try:
        response = httpx.post("http://aiproxy.sanand.workers.dev/openai/v1/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No answer found.")
        if result == "No answer found.":
            raise Exception("Block 1 did not process the input correctly.")
        return result
    except Exception as e:
        return f"Error: {str(e)}"
