import os
import httpx

def ask_gpt(instruction, question):
    """Send a minimal request to OpenAI GPT-4o Mini."""
    headers = {"Authorization": f"Bearer {os.environ.get("AIPROXY_TOKEN")}", "Content-Type": "application/json"}
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
