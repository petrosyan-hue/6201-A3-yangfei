import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.assistant import answer_question
from src.retrieval import load_faq


def contains_all(answer: str, expected_terms: list[str]) -> bool:
    lowered = answer.lower()
    return all(term.lower() in lowered for term in expected_terms)


def main() -> None:
    entries = load_faq(ROOT / "data" / "faq.json")
    cases = json.loads((ROOT / "eval" / "eval_cases.json").read_text(encoding="utf-8"))
    results = []
    total_latency = 0.0
    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0.0

    for case in cases:
        response = answer_question(case["question"], entries)
        source_ok = response.source_id == case["expected_source_id"]
        content_ok = contains_all(response.answer, case["must_contain"])
        passed = source_ok and content_ok
        total_latency += response.metrics.latency_seconds
        total_input_tokens += response.metrics.input_tokens
        total_output_tokens += response.metrics.output_tokens
        total_cost += response.metrics.estimated_cost_usd
        results.append(
            {
                "id": case["id"],
                "passed": passed,
                "source_ok": source_ok,
                "content_ok": content_ok,
                "expected_source_id": case["expected_source_id"],
                "actual_source_id": response.source_id,
                "answer": response.answer,
                "latency_seconds": response.metrics.latency_seconds,
                "input_tokens": response.metrics.input_tokens,
                "output_tokens": response.metrics.output_tokens,
                "estimated_cost_usd": response.metrics.estimated_cost_usd,
            }
        )

    passed_count = sum(1 for result in results if result["passed"])
    print(f"Pass rate: {passed_count}/{len(results)} = {passed_count / len(results):.0%}")
    print(f"Average latency: {total_latency / len(results):.4f}s")
    print(f"Average input tokens: {total_input_tokens / len(results):.1f}")
    print(f"Average output tokens: {total_output_tokens / len(results):.1f}")
    print(f"Total estimated cost: ${total_cost:.8f}")
    print()
    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"{status} {result['id']}: expected={result['expected_source_id']} actual={result['actual_source_id']}")

    output_path = ROOT / "eval" / "eval_results.json"
    output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved detailed results to {output_path}")


if __name__ == "__main__":
    main()
