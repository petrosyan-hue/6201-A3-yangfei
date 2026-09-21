import re
import time
from contextlib import contextmanager
from dataclasses import dataclass


WORD_RE = re.compile(r"\w+|[\u4e00-\u9fff]")


@dataclass
class RunMetrics:
    input_tokens: int
    output_tokens: int
    latency_seconds: float
    estimated_cost_usd: float


@contextmanager
def timer():
    start = time.perf_counter()
    result = {"elapsed": 0.0}
    try:
        yield result
    finally:
        result["elapsed"] = time.perf_counter() - start


def estimate_tokens(text: str) -> int:
    # Approximation for reporting. Real API tokenizers differ by model.
    return len(WORD_RE.findall(text))


def estimate_cost(input_tokens: int, output_tokens: int) -> float:
    # Conservative placeholder price for a low-cost model:
    # input US$0.50/M tokens, output US$1.50/M tokens.
    input_cost = input_tokens / 1_000_000 * 0.50
    output_cost = output_tokens / 1_000_000 * 1.50
    return input_cost + output_cost
