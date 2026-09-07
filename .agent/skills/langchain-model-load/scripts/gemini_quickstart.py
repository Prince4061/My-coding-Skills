import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. .env file se environment variables load karo
load_dotenv()

# Check karo ki API key available hai ya nahi
if not os.getenv("GOOGLE_API_KEY"):
    print("\n[ERROR] GOOGLE_API_KEY nahi mili!")
    print("Kripya project folder me '.env' file banayein aur usme likhein:")
    print("GOOGLE_API_KEY=your_actual_gemini_api_key\n")
    sys.exit(1)

# 2. Gemini model initialize karo
# gemini-1.5-flash fast aur cost-effective model hai
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3
)

# 3. Model se direct sawal puchho (Single-turn)
prompt = "Python me list aur tuple me kya farak hai? 2 line me samjhao."
print(f"Question: {prompt}\n")

response = llm.invoke(prompt)

# 4. Javab screen par print karo
print("Answer:")
print(response.content)
