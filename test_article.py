import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY is missing in your .env file")

client = OpenAI(api_key=api_key)


def generate_article(topic: str) -> str:
    prompt = f"""
You are a professional article writer.

Write a complete article about:

"{topic}"

Requirements:
- Strong title
- Introduction
- 4 main sections with headings
- Simple explanations
- Practical examples
- Conclusion
- Use a professional but easy-to-understand tone
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text


def main():
    print("===================================")
    print("📝 OpenAI Article Generator Test")
    print("===================================")

    topic = input("Enter your article topic: ").strip()

    if not topic:
        print("❌ You did not enter a topic.")
        return

    print("\n⏳ Generating article...\n")

    try:
        article = generate_article(topic)
        print(article)

        with open("generated_article.txt", "w", encoding="utf-8") as file:
            file.write(article)

        print("\n✅ Article saved to generated_article.txt")

    except Exception as e:
        print("❌ Error while generating article:")
        print(e)


if __name__ == "__main__":
    main()