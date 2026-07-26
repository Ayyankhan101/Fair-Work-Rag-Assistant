#!/usr/bin/env python3
"""Check Groq API rate limit status."""
import os
import sys
from dotenv import load_dotenv

def main():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY not set in .env")
        return 1

    from groq import Groq
    client = Groq(api_key=api_key)

    models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    for model in models:
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Say OK"}],
                max_tokens=5,
            )
            print(f"{model}: OK")
        except Exception as e:
            err = str(e)
            if "429" in err:
                # Extract wait time
                import re
                match = re.search(r"try again in ([\d.]+)", err)
                wait = match.group(1) if match else "?"
                print(f"{model}: BLOCKED (wait {wait}s)")
            else:
                print(f"{model}: ERROR - {err[:100]}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
