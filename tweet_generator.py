import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = os.getenv('GROQ_API_URL', 'https://api.groq.com/openai/v1/chat/completions')
LLAMA_MODEL = os.getenv('LLAMA_MODEL', 'llama-3.1-8b-instant')
TELEGRAM_BOT_TOKEN = os.getenv('BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('CHAT_ID')

def generate_tweet_idea(topic):
    """Return the topic and a prompt for a catchy tweet idea."""
    prompt = f"Generate a catchy tweet idea about {topic}."  # For header
    return topic, prompt

def generate_tweet_content(topic, affiliate_link=None):
    print(f"[INFO] Generating single tweet for topic: '{topic}' | Affiliate link: {affiliate_link}")
    # Eye-catching title
    title = f"🔥 {topic.title()} - Top 5 Commands You Must Know!"
    # Compose prompt for a single, well-structured tweet
    prompt = (
        f"Write a single, perfect tweet for the topic: '{topic}'.\n"
        f"- Start with an eye-catching title: {title}\n"
        "- List the top 5 commands as bullet points, each with a short description.\n"
        "- Use relevant emojis for each command.\n"
        "- End with a strong closing line, a call to action, and 2-3 relevant hashtags.\n"
        f"- If an affiliate link is provided, add it at the end with a call to check it out: {affiliate_link if affiliate_link else ''}"
    )
    data = {
        "model": LLAMA_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for tech Twitter content. Always use engaging hooks, emojis, bullet points, and clear formatting. The tweet should be visually appealing and actionable."},
            {"role": "user", "content": prompt}
        ]
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    print(f"[DEBUG] Sending request to Groq API for single tweet...")
    response = requests.post(GROQ_API_URL, json=data, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] Groq API error for single tweet: {response.text}")
        raise e
    tweet = response.json()['choices'][0]['message']['content'].strip()
    print(f"[INFO] Single tweet generated: {tweet}")
    return tweet

def handle_telegram_message(topic, affiliate_link=None):
    print(f"[INFO] handle_telegram_message called with topic: '{topic}', affiliate_link: {affiliate_link}")
    tweet = generate_tweet_content(topic, affiliate_link=affiliate_link)
    print(f"[INFO] Final tweet to send:\n{tweet}")
    return tweet

def main():
    if not GROQ_API_KEY:
        print("Error: GROQ_API_KEY environment variable not set.")
        return
    # This main is now for manual testing only. Telegram bot should call handle_telegram_message directly.
    print("This script is designed to be used as a module in your Telegram bot.")
    print("Import and call handle_telegram_message(topic, affiliate_link) from your bot handler.")

if __name__ == "__main__":
    main()
