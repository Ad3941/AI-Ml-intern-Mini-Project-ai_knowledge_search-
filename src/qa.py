from typing import List, Dict, Tuple
from src.config import OPENAI_API_KEY, ANTHROPIC_API_KEY

def generate_answer(query: str, retrieved_chunks: List[Dict[str, any]], scores: List[float]) -> Tuple[str, str]:
    """Generates an answer using LLM if keys are configured, otherwise uses extractive fallback."""
    if not retrieved_chunks:
        return "I could not find any relevant information in the uploaded documents matching your query.", "none"

    context_str = "\n\n".join([
        f"[Source {i+1} - {chunk['source']} | Similarity: {scores[i]:.2f}]\n{chunk['text']}"
        for i, chunk in enumerate(retrieved_chunks)
    ])

    system_prompt = (
        "You are an expert AI assistant. Answer the user's question strictly using ONLY the provided context below. "
        "If the answer cannot be found fully within the context, state: 'I don't know based on the provided documents.'"
    )

    # Try OpenAI
    if OPENAI_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.messages.create(  # type: ignore
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Context:\n{context_str}\n\nQuestion: {query}"}
                ],
                temperature=0.0
            )
            return response.choices[0].message.content, "openai" # type: ignore
        except Exception:
            pass # Fallback if API call fails

    # Try Anthropic
    if ANTHROPIC_API_KEY:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": f"Context:\n{context_str}\n\nQuestion: {query}"}
                ]
            )
            return response.content[0].text, "anthropic"
        except Exception:
            pass

    # Extractive Fallback Mode (Offline Demo)
    extractive_summary = (
        "**[Extractive Offline Mode - No LLM API Key detected]**\n\n"
        f"Based on the most relevant passage from **{retrieved_chunks[0]['source']}**:\n\n"
        f"> \"{retrieved_chunks[0]['text']}\""
    )
    return extractive_summary, "extractive"