import time
import os
from openai import OpenAI
from openai import RateLimitError

def get_openai_response(prompt, retries=3, delay=5):
    """Fetches a response from OpenAI API based on the prompt provided using chat completions."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    for attempt in range(retries):
        try:
            # Delay between retries
            time.sleep(1)  # Adjust to manage rate limits
            
            # OpenAI chat completion request
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024,
            )
            return response.choices[0].message.content.strip()
        
        except RateLimitError:
            print(f"Rate limit exceeded. Retrying in {delay} seconds (Attempt {attempt + 1} of {retries})...")
            time.sleep(delay)
    
    return "Request failed after multiple attempts due to rate limit issues."
