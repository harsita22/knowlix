"""Gemini LLM wrapper for Knowlix. Pure Google Gemini integration with 429 retry backoff."""
import json
import os
import random
import time

import config


class LLM:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("No GEMINI_API_KEY found. Set GEMINI_API_KEY in .env (get a free key at https://aistudio.google.com/apikey).")
        from google import genai
        self.client = genai.Client(api_key=api_key)
        self.model = config.GEMINI_MODEL

    def generate(self, system, messages):
        """messages: list of {"role": "user"|"assistant", "content": str}. Returns text. Retries on 429 / rate limits."""
        max_attempts = 4
        for attempt in range(max_attempts):
            try:
                return self._call(system, messages)
            except Exception as e:
                err_str = str(e).lower()
                is_rate_limit = "429" in err_str or "rate" in err_str or "quota" in err_str or "resource_exhausted" in err_str
                if attempt < max_attempts - 1 and is_rate_limit:
                    sleep_time = (2 ** attempt) * 2 + random.uniform(0.1, 1.0)
                    time.sleep(sleep_time)
                    continue
                # On non-rate-limit errors or after retries exhausted, raise with clean message
                raise RuntimeError(f"Gemini generation error: {e}")

    def _call(self, system, messages):
        from google.genai import types
        text = "\n\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages)
        response = self.client.models.generate_content(
            model=self.model,
            contents=text,
            config=types.GenerateContentConfig(
                system_instruction=system,
                temperature=config.TEMPERATURE
            )
        )
        return response.text or ""

    def embed(self, text):
        """Compute text embedding using Gemini embedding model."""
        if not text or not str(text).strip():
            return []
        try:
            response = self.client.models.embed_content(
                model=config.GEMINI_EMBEDDING_MODEL,
                contents=str(text)
            )
            # Support both object and list embedding responses from SDK
            if hasattr(response, "embedding") and response.embedding:
                return response.embedding.values if hasattr(response.embedding, "values") else list(response.embedding)
            if hasattr(response, "embeddings") and response.embeddings:
                emb = response.embeddings[0]
                return emb.values if hasattr(emb, "values") else list(emb)
            return []
        except Exception as e:
            # Fallback gracefully if embedding is unavailable
            return []


class DryRunLLM:
    """Scripted stand-in so you can test your setup with NO API key: python main.py --dry-run "..." """

    def __init__(self):
        self.step = 0

    def generate(self, system, messages):
        self.step += 1
        if self.step == 1:
            return '{"thought": "See which data files exist.", "action": "list_files", "args": {}}'
        if self.step == 2:
            return '{"thought": "Check a calculation.", "action": "calculator", "args": {"expression": "2 + 2 * 10"}}'
        return '{"thought": "I have enough.", "final_answer": "Dry run OK: tools executed (list_files, calculator)."}'

    def embed(self, text):
        return [0.0] * 768
