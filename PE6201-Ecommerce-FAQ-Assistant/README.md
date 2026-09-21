# 6201-A3-yangfei

## PE6201 End-of-Course Project

### AI Multilingual FAQ Assistant for Cross-Border E-commerce

This project builds a small multilingual FAQ assistant for cross-border e-commerce support. It retrieves the most relevant FAQ entry and answers in the user's language when possible. If the evidence is weak, it refuses to guess and asks the user to contact support.

## Why this project

Cross-border e-commerce customers may ask simple support questions in different languages. FAQ information is often scattered across policy pages, shipping pages and return pages, so customers may receive slow or inconsistent answers. A small retrieval-based assistant can make common support information easier to find while keeping answers grounded in approved FAQ records.

## What it does

- Reads a small FAQ knowledge base from `data/faq.json`.
- Accepts English, Chinese or Spanish customer questions.
- Retrieves the best matching FAQ entry.
- Produces a short answer and cites the FAQ source.
- Refuses to answer when no FAQ entry is relevant enough.
- Records approximate tokens, latency and estimated cost.
- Runs an evaluation harness over test cases in `eval/eval_cases.json`.

## How to run

```bash
python3 app.py
```

## How to run the web demo

Install the optional web dependency:

```bash
python3 -m pip install -r requirements.txt
```

Then run:

```bash
python3 -m streamlit run web_app.py
```

Example questions:

```text
Can I return an item after 14 days?
我的包裹丢了怎么办？
¿Cuánto tarda el envío internacional?
```

## How to run the evaluation harness

```bash
python3 eval/run_eval.py
```

The evaluation prints pass rate, average latency, average token estimate and estimated cost.

## Project structure

```text
.
├── app.py
├── web_app.py
├── src/
│   ├── assistant.py
│   ├── retrieval.py
│   └── metrics.py
├── data/
│   └── faq.json
├── eval/
│   ├── eval_cases.json
│   └── run_eval.py
├── requirements.txt
└── README.md
```

## Notes

This first version uses deterministic local retrieval and template answers. It does not require an API key, so it can run on another machine without paid services. The report can discuss a later LLM version as a trade-off: a model may improve natural phrasing and translation, but it also adds token cost, latency and hallucination risk.

## Current measured result

The latest evaluation run passed all 10 scripted cases:

```text
Pass rate: 10/10 = 100%
Average latency: 0.0002s
Average input tokens: 24.1
Average output tokens: 19.3
Total estimated cost: $0.00041000
```
