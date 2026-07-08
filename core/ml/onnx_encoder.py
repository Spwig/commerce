"""
Lightweight ONNX-based sentence encoder for help system semantic search.

Replaces sentence-transformers + PyTorch (~2-3GB) with onnxruntime + tokenizers (~55MB).
Uses the same all-MiniLM-L6-v2 model exported to ONNX format.

The model files are located at core/ml/help_search/ and include:
- model.onnx + model.onnx.data: The transformer model
- tokenizer.json: HuggingFace fast tokenizer
- encoder_config.json: Model configuration
"""

import json
import logging
from pathlib import Path
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)

# Default model directory relative to this file
DEFAULT_MODEL_DIR = Path(__file__).parent / 'help_search'


class OnnxSentenceEncoder:
    """
    Singleton ONNX-based sentence encoder.
    Lazy-loaded to avoid startup overhead (same pattern as the old SentenceTransformerModel).
    """
    _instance = None
    _session = None
    _tokenizer = None
    _config = None

    @classmethod
    def get_instance(cls, model_dir: Optional[Path] = None):
        """Get or create the singleton instance."""
        if cls._instance is None:
            cls._instance = cls(model_dir or DEFAULT_MODEL_DIR)
        return cls._instance

    def __init__(self, model_dir: Path):
        """Initialize and load ONNX model + tokenizer."""
        if self.__class__._session is not None:
            return

        model_dir = Path(model_dir)

        # Load config
        config_path = model_dir / 'encoder_config.json'
        if not config_path.exists():
            raise FileNotFoundError(
                f"Encoder config not found: {config_path}. "
                f"Run 'python scripts/export_model_to_onnx.py' to generate model files."
            )

        with open(config_path) as f:
            self.__class__._config = json.load(f)

        # Load ONNX model
        onnx_path = model_dir / self._config['onnx_file']
        if not onnx_path.exists():
            raise FileNotFoundError(f"ONNX model not found: {onnx_path}")

        try:
            import onnxruntime as ort
            logger.info(f"Loading ONNX model: {onnx_path.name}")
            self.__class__._session = ort.InferenceSession(
                str(onnx_path),
                providers=['CPUExecutionProvider'],
            )
            logger.info("ONNX model loaded successfully")
        except ImportError:
            raise ImportError(
                "onnxruntime not installed. Install with: pip install onnxruntime"
            )

        # Load tokenizer
        tokenizer_path = model_dir / 'tokenizer.json'
        if not tokenizer_path.exists():
            raise FileNotFoundError(f"Tokenizer not found: {tokenizer_path}")

        try:
            from tokenizers import Tokenizer
            self.__class__._tokenizer = Tokenizer.from_file(str(tokenizer_path))
            max_length = self._config.get('max_seq_length', 256)
            self.__class__._tokenizer.enable_truncation(max_length=max_length)
            self.__class__._tokenizer.enable_padding(length=None)
            logger.info("Tokenizer loaded successfully")
        except ImportError:
            raise ImportError(
                "tokenizers not installed. Install with: pip install tokenizers"
            )

    def encode(self, text: str) -> np.ndarray:
        """
        Generate embedding for text.

        Args:
            text: Input text to encode

        Returns:
            384-dimensional numpy array (normalized)
        """
        dimensions = self._config.get('dimensions', 384)

        # Normalize text
        text = text.strip()
        if not text:
            return np.zeros(dimensions, dtype=np.float32)

        # Tokenize
        encoding = self._tokenizer.encode(text)

        input_ids = np.array([encoding.ids], dtype=np.int64)
        attention_mask = np.array([encoding.attention_mask], dtype=np.int64)
        token_type_ids = np.array([encoding.type_ids], dtype=np.int64)

        # Run ONNX inference
        outputs = self._session.run(
            ['last_hidden_state'],
            {
                'input_ids': input_ids,
                'attention_mask': attention_mask,
                'token_type_ids': token_type_ids,
            }
        )

        # Mean pooling over token embeddings (masked)
        token_embeddings = outputs[0]  # (1, seq_len, hidden_dim)
        mask_expanded = attention_mask[:, :, np.newaxis].astype(np.float32)
        sum_embeddings = np.sum(token_embeddings * mask_expanded, axis=1)
        sum_mask = np.clip(mask_expanded.sum(axis=1), a_min=1e-9, a_max=None)
        embedding = (sum_embeddings / sum_mask)[0]  # (hidden_dim,)

        # Normalize
        if self._config.get('normalize_embeddings', True):
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm

        return embedding
