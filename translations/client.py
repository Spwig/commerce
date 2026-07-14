"""
Client for communicating with the translator microservice
"""

import logging
import os
import re

import httpx

logger = logging.getLogger(__name__)


class TranslatorClient:
    """Client for the translator microservice"""

    def __init__(self):
        # Auto-detect if running in Docker or locally
        default_url = "http://translator:8088"
        if not os.path.exists("/.dockerenv"):
            # Running outside Docker, use localhost
            default_url = "http://localhost:8088"

        self.base_url = os.getenv("TRANSLATOR_URL", default_url)
        self.enabled = os.getenv("TRANSLATOR_ENABLED", "true").lower() == "true"
        self.timeout = 30.0
        self._api_key = os.getenv("TRANSLATOR_API_KEY", "")

    def _headers(self) -> dict:
        """Return auth headers for translator API requests"""
        if self._api_key:
            return {"X-API-Key": self._api_key}
        return {}

    def _split_into_sentences(self, text: str) -> list[tuple[str, bool]]:
        """
        Split text into sentences while preserving formatting.

        Returns list of tuples: (text_chunk, is_sentence)
        - is_sentence=True: actual sentence to translate
        - is_sentence=False: whitespace/formatting to preserve as-is

        This fixes the multi-sentence translation issue where sentence transformers
        only translate the first sentence when multiple are sent together.
        """
        if not text or not text.strip():
            return [(text, False)]

        # Pattern to split on sentence boundaries while preserving whitespace
        # Matches sentence-ending punctuation from various writing systems followed by space/newline
        # Includes: Latin, Chinese, Japanese, Arabic, Greek, Armenian, Ethiopic, Thai, Devanagari, etc.
        sentence_pattern = r"(?<=[.!?。！？؟۔։֊።፧፨ฯ।॥])(?=\s+|$)"

        # First check for common abbreviations that shouldn't split sentences
        abbreviations = r"\b(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|vs|etc|e\.g|i\.e|Inc|Ltd|Co)\."

        # Replace abbreviations temporarily to protect them
        protected_text = text
        abbreviation_matches = list(re.finditer(abbreviations, text, re.IGNORECASE))
        placeholders = {}
        for i, match in enumerate(abbreviation_matches):
            placeholder = f"__ABBR_{i}__"
            placeholders[placeholder] = match.group()
            protected_text = protected_text.replace(match.group(), placeholder)

        # Split into chunks (sentences + whitespace)
        chunks = []
        last_end = 0

        # Find sentence boundaries
        for match in re.finditer(sentence_pattern, protected_text):
            sentence_end = match.start()

            # Extract the sentence
            sentence = protected_text[last_end:sentence_end].strip()

            if sentence:
                # Restore abbreviations in sentence
                for placeholder, original in placeholders.items():
                    sentence = sentence.replace(placeholder, original)

                chunks.append((sentence, True))  # This is a sentence

                # Extract and preserve whitespace after sentence
                whitespace_end = match.end()
                while (
                    whitespace_end < len(protected_text)
                    and protected_text[whitespace_end].isspace()
                ):
                    whitespace_end += 1

                if whitespace_end > match.end():
                    whitespace = protected_text[match.end() : whitespace_end]
                    chunks.append((whitespace, False))  # Preserve whitespace

                last_end = whitespace_end

        # Handle any remaining text
        if last_end < len(protected_text):
            remaining = protected_text[last_end:].strip()
            if remaining:
                # Restore abbreviations
                for placeholder, original in placeholders.items():
                    remaining = remaining.replace(placeholder, original)
                chunks.append((remaining, True))

        # If no sentences found, treat entire text as one sentence
        if not chunks:
            chunks = [(text, True)]

        return chunks

    def is_available(self) -> bool:
        """Check if the translator service is available"""
        if not self.enabled:
            return False

        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.base_url}/health")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Translator service health check failed: {e}")
            return False

    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        glossary: dict[str, str] | None = None,
    ) -> str | None:
        """
        Translate text using the translator service.

        Automatically handles multi-sentence text by splitting sentences and using
        batch translation to work around sentence transformer limitations.
        """
        if not self.enabled:
            logger.warning("Translator service is disabled")
            return None

        # Check if text ends with sentence-ending punctuation from any language
        # If not, add a period to ensure proper translation by sentence transformers
        text_to_translate = text
        added_punctuation = False

        # Comprehensive list of sentence-ending punctuation from various writing systems
        # Latin: . ! ?
        # Chinese/Japanese: 。！？
        # Arabic: ؟ ۔
        # Greek: ; (Greek question mark is semicolon)
        # Armenian: ։ ֊
        # Ethiopic: ። ፧ ፨
        # Thai: ฯ
        # Devanagari: । ॥
        # And more...
        sentence_end_pattern = r"[.!?。！？؟۔։֊።፧፨ฯ।॥]$"

        if text.strip() and not re.search(sentence_end_pattern, text.strip()):
            text_to_translate = text.strip() + "."
            added_punctuation = True
            logger.debug("Added sentence-ending punctuation for proper translation")

        # Split text into sentences
        chunks = self._split_into_sentences(text_to_translate)

        # Count actual sentences (not whitespace)
        sentences = [chunk for chunk, is_sentence in chunks if is_sentence]

        # If only one sentence, use single translation endpoint
        if len(sentences) <= 1:
            result = self._translate_single(text_to_translate, source_lang, target_lang, glossary)

            # Remove added punctuation from result if we added it
            # We only remove the Latin period (.) that we added, not other punctuation
            if result and added_punctuation:
                # Check if result ends with a Latin period (the one we added)
                if result.rstrip().endswith("."):
                    result = result.rstrip()[:-1].rstrip()

            return result

        # Multiple sentences - use batch translation to fix sentence transformer issue
        logger.debug(f"Translating {len(sentences)} sentences using batch API")

        try:
            # Prepare batch items (only translate actual sentences, not whitespace)
            batch_items = []
            for i, (chunk_text, is_sentence) in enumerate(chunks):
                if is_sentence:
                    batch_items.append(
                        {
                            "id": str(i),
                            "text": chunk_text,
                            "source_lang": source_lang,
                            "target_lang": target_lang,
                        }
                    )

            # Call batch translation API
            batch_results = self.translate_batch(batch_items, glossary)

            # Build result lookup by ID
            translations = {
                item["id"]: item.get("translated_text", "")
                for item in batch_results
                if item.get("success")
            }

            # Reconstruct text with translations
            result_parts = []
            for i, (chunk_text, is_sentence) in enumerate(chunks):
                if is_sentence:
                    # Use translated text
                    translated = translations.get(
                        str(i), chunk_text
                    )  # Fallback to original if translation failed
                    result_parts.append(translated)
                else:
                    # Preserve whitespace as-is
                    result_parts.append(chunk_text)

            final_text = "".join(result_parts)

            # Remove added punctuation from result if we added it
            # We specifically check for Latin period (.) since that's what we always add,
            # regardless of the source language
            if added_punctuation and final_text.rstrip().endswith("."):
                final_text = final_text.rstrip()[:-1].rstrip()

            logger.debug(f"Multi-sentence translation successful: {len(sentences)} sentences")
            return final_text

        except Exception as e:
            logger.error(f"Multi-sentence translation failed: {e}")
            # Fallback to single translation (will only translate first sentence, but better than nothing)
            logger.warning("Falling back to single translation endpoint")
            result = self._translate_single(text_to_translate, source_lang, target_lang, glossary)

            # Remove added punctuation from result if we added it
            # We specifically check for Latin period (.) since that's what we always add,
            # regardless of the source language
            if result and added_punctuation and result.rstrip().endswith("."):
                result = result.rstrip()[:-1].rstrip()

            return result

    def _translate_single(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        glossary: dict[str, str] | None = None,
    ) -> str | None:
        """Translate a single text using the single translation endpoint"""
        # Build request data, excluding None values
        request_data = {"text": text, "source_lang": source_lang, "target_lang": target_lang}
        if glossary is not None:
            request_data["glossary"] = glossary

        logger.debug(f"Translation request: {request_data}")

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/translate", json=request_data, headers=self._headers()
                )

                # Log response for debugging
                logger.debug(f"Translation response status: {response.status_code}")

                if response.status_code == 422:
                    # Log the validation error details
                    error_detail = response.json()
                    logger.error(f"Translation validation error (422): {error_detail}")
                    logger.error(
                        f"Request was: text='{text[:50]}...', source={source_lang}, target={target_lang}"
                    )
                    return None

                response.raise_for_status()
                result = response.json()
                logger.debug(
                    f"Translation successful: {target_lang} -> {result.get('translated_text', '')[:50]}..."
                )
                return result["translated_text"]
        except httpx.TimeoutException:
            logger.error(f"Translation timeout for text: {text[:50]}...")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"Translation HTTP error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return None

    def translate_batch(
        self, items: list[dict], glossary: dict[str, str] | None = None
    ) -> list[dict]:
        """Translate multiple texts in batch"""
        if not self.enabled:
            logger.warning("Translator service is disabled")
            return []

        try:
            with httpx.Client(timeout=self.timeout * 2) as client:
                response = client.post(
                    f"{self.base_url}/translate_batch",
                    json={"items": items, "glossary": glossary},
                    headers=self._headers(),
                )
                response.raise_for_status()
                return response.json()["results"]
        except Exception as e:
            logger.error(f"Batch translation failed: {e}")
            return []

    def get_models(self) -> list[dict]:
        """Get list of installed models"""
        if not self.enabled:
            return []

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{self.base_url}/models")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to get models: {e}")
            return []

    def run_benchmark(
        self,
        source_lang: str,
        target_lang: str,
        num_samples: int = 50,
        sample_length: str = "medium",
    ) -> dict | None:
        """Run a translation benchmark"""
        if not self.enabled:
            return None

        try:
            with httpx.Client(timeout=self.timeout * 3) as client:
                response = client.post(
                    f"{self.base_url}/benchmark",
                    json={
                        "language_pair": f"{source_lang}-{target_lang}",
                        "num_samples": num_samples,
                        "sample_length": sample_length,
                    },
                    headers=self._headers(),
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Benchmark failed: {e}")
            return None

    def get_system_info(self) -> dict | None:
        """Get system information from the translator service"""
        if not self.enabled:
            return None

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{self.base_url}/health")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to get system info: {e}")
            return None

    def get_download_status(self) -> dict | None:
        """Get model download status"""
        if not self.enabled:
            return None

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{self.base_url}/download/status")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to get download status: {e}")
            return None

    def start_download(self) -> bool:
        """Start model download"""
        if not self.enabled:
            return False

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(f"{self.base_url}/download/start", headers=self._headers())
                response.raise_for_status()
                return True
        except Exception as e:
            logger.error(f"Failed to start download: {e}")
            return False

    def clear_cache(self) -> bool:
        """Clear the translation cache"""
        if not self.enabled:
            return False

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(f"{self.base_url}/cache/clear", headers=self._headers())
                response.raise_for_status()
                return True
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")
            return False

    def _request(self, method: str, endpoint: str, **kwargs) -> dict | None:
        """Make a generic request to the translator service"""
        if not self.enabled:
            return None

        try:
            # Merge auth headers with any caller-provided headers
            headers = self._headers()
            if "headers" in kwargs:
                headers.update(kwargs.pop("headers"))
            with httpx.Client(timeout=self.timeout) as client:
                url = f"{self.base_url}{endpoint}"
                response = client.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return None

    def get_full_status(self) -> dict | None:
        """Get complete system status in one call (optimized)"""
        if not self.enabled:
            return None

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{self.base_url}/system/full-status")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to get full status: {e}")
            return None


# Global client instance
_client = None


def get_translator_client() -> TranslatorClient:
    """Get or create the global translator client"""
    global _client
    if _client is None:
        _client = TranslatorClient()
    return _client
