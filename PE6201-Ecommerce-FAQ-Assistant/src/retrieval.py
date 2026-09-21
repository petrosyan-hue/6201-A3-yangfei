import json
import re
from dataclasses import dataclass
from pathlib import Path


TOKEN_RE = re.compile(r"[a-z0-9]+|[\u4e00-\u9fff]+", re.IGNORECASE)
STOPWORDS = {
    "a", "an", "and", "are", "can", "do", "does", "for", "has", "have", "how",
    "i", "if", "in", "is", "it", "my", "of", "on", "or", "the", "to", "what",
    "when", "where", "which", "who", "with", "you", "your"
}

TOPIC_KEYWORDS = {
    "returns": {"return", "returns", "refund", "unused", "packaging", "退货"},
    "shipping": {"shipping", "delivery", "international", "物流", "배송"},
    "lost_package": {"lost", "package", "parcel", "tracking", "包裹", "丢"},
    "cancellation": {"cancel", "cancelar", "cancellation", "取消", "pedido"},
    "customs": {"customs", "duties", "taxes", "import", "关税", "进口税"},
    "payment": {"payment", "pay", "card", "cards", "wallet", "methods", "付款"},
    "warranty": {"warranty", "defects", "electronics", "保修"},
}


@dataclass
class FAQEntry:
    id: str
    topic: str
    language: str
    question: str
    answer: str
    source: str


def load_faq(path: str | Path) -> list[FAQEntry]:
    with open(path, encoding="utf-8") as f:
        rows = json.load(f)
    return [FAQEntry(**row) for row in rows]


def tokenize(text: str) -> set[str]:
    text = text.lower()
    tokens = {token for token in TOKEN_RE.findall(text) if token not in STOPWORDS}
    # Add single Chinese characters as fallback so Chinese questions can still match.
    for char in text:
        if "\u4e00" <= char <= "\u9fff":
            tokens.add(char)
    return tokens


def detect_language(text: str) -> str:
    if any("\u4e00" <= char <= "\u9fff" for char in text):
        return "zh"
    spanish_marks = {"¿", "¡", "pedido", "envío", "cancelar", "cuánto"}
    lowered = text.lower()
    if any(mark in lowered for mark in spanish_marks):
        return "es"
    return "en"


def score_entry(query: str, entry: FAQEntry) -> float:
    query_terms = tokenize(query)
    doc_terms = tokenize(f"{entry.topic} {entry.question} {entry.answer}")
    if not query_terms or not doc_terms:
        return 0.0
    overlap = len(query_terms & doc_terms)
    base = overlap / len(query_terms)
    topic_terms = TOPIC_KEYWORDS.get(entry.topic, set())
    if query_terms & topic_terms:
        base += 0.35
    # Prefer entries in the user's language when evidence strength is otherwise similar.
    if detect_language(query) == entry.language:
        base += 0.15
    return base


def retrieve(query: str, entries: list[FAQEntry], threshold: float = 0.18) -> tuple[FAQEntry | None, float]:
    scored = sorted(((score_entry(query, entry), entry) for entry in entries), reverse=True, key=lambda x: x[0])
    if not scored or scored[0][0] < threshold:
        return None, scored[0][0] if scored else 0.0
    return scored[0][1], scored[0][0]
