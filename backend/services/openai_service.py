import os
from dotenv import load_dotenv

load_dotenv()

def classify_document(text: str):
    """Classify document using OpenAI. Falls back to basic classification if API is unavailable."""
    try:
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("No OpenAI API key configured")

        client = OpenAI(api_key=api_key)
        truncated_text = text[:3000]

        prompt = f"""
        Classify this document into one of:
        Finance, Legal, Crypto, Social, Personal.

        Also give a one-line summary.

        Text:
        {truncated_text}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
        )

        output = response.choices[0].message.content

        # Basic parsing
        lines = output.split("\n")
        category = lines[0].strip()
        summary = lines[-1].strip()

        return category, summary

    except Exception as e:
        print(f"[OpenAI] Classification failed ({type(e).__name__}): {e}")
        print("[OpenAI] Using fallback classification")

        # Fallback: basic keyword-based classification
        text_lower = text.lower()
        if any(w in text_lower for w in ["invoice", "bank", "tax", "payment", "financial", "salary", "budget"]):
            category = "Finance"
        elif any(w in text_lower for w in ["contract", "agreement", "legal", "court", "law", "clause"]):
            category = "Legal"
        elif any(w in text_lower for w in ["crypto", "bitcoin", "ethereum", "blockchain", "wallet", "token"]):
            category = "Crypto"
        elif any(w in text_lower for w in ["friend", "family", "social", "message", "chat"]):
            category = "Social"
        else:
            category = "Personal"

        # Fallback summary: first 100 chars
        summary = text[:100].strip().replace("\n", " ")
        if len(text) > 100:
            summary += "..."

        return category, summary