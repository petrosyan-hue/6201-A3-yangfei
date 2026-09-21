# AI Multilingual FAQ Assistant for Cross-Border E-commerce

## Problem and significance

Cross-border e-commerce customers often ask simple support questions in different languages, but the answer may be scattered across return, shipping, customs, payment and warranty pages. This creates slow or inconsistent support, especially when the customer cannot easily read the store's main support language. The project therefore builds a small multilingual FAQ assistant that helps customers find approved policy information quickly while reducing unsupported answers.

## Why AI and which kind

A simple keyword search can match obvious phrases such as "return" or "shipping", but it is weak when customers paraphrase, mix languages or ask a question in Chinese or Spanish. A pure foundation-model answer is also risky because it may invent a return or customs policy that the store has not approved. I therefore chose a retrieval-grounded assistant. The system first retrieves the most relevant FAQ record, then answers only from that evidence. If no FAQ record is relevant enough, it refuses to answer and asks the customer to contact support.

This is not a full autonomous agent. The task does not need multi-step planning or irreversible action. It needs grounded retrieval, multilingual wording and safe refusal. This keeps the system smaller, cheaper and easier to test.

## Build vs buy trade-off

The project owns the FAQ data, retrieval logic, refusal threshold, evaluation harness and demo interface. It rents nothing in the first version, so it runs without an API key and can be reproduced on another machine. A commercial chatbot platform would provide a nicer interface and stronger natural language generation, but it would hide the retrieval logic and make cost harder to inspect. A later version could rent a foundation model only for paraphrasing a grounded answer, while keeping retrieval, refusal rules and evaluation under project control.

## Data and implementation

The prototype uses a small FAQ knowledge base with return, shipping, lost package, cancellation, customs, payment and warranty entries in English, Chinese and Spanish. The assistant tokenises the customer question, detects the likely language, scores FAQ entries by word overlap and topic keywords, and returns the highest-scoring entry only if it passes a relevance threshold. The answer includes the FAQ source. If the score is too low, the system refuses instead of guessing.

The implementation has two interfaces. The command-line version is used for reproducibility. The Streamlit web version is used for the recorded demo because it shows the answer, source, confidence, latency, estimated tokens and estimated cost on one screen.

## Evaluation and measured results

I built a 10-case evaluation harness. Each case specifies a customer question, the expected FAQ source and required answer terms. The harness runs every case, checks whether the retrieved source and answer content match, and records pass rate, approximate input tokens, output tokens, latency and estimated cost.

The current version passed 10/10 cases. Average latency was 0.0002 seconds. Average input was 24.1 estimated tokens and average output was 19.3 estimated tokens. Total estimated cost for the 10-case run was USD 0.000410. These figures are small because the current prototype uses local retrieval and template answers rather than a live model. The useful result is not that the system is already production-ready, but that the evaluation harness makes failures visible and repeatable.

The harness also shaped the build. An earlier retrieval version passed only 7/10 cases because common words caused the wrong FAQ to be selected. Adding stopwords and topic keywords raised the measured pass rate to 10/10. This is the main evidence that evaluation improved the system rather than merely describing it.

## Risks and responsible use

The system should not be deployed as a final customer-service replacement. The FAQ set is small, the token estimate is approximate, and the multilingual coverage is limited. Retrieval can still fail if a customer asks a mixed-intent question or uses wording that the FAQ does not cover. The assistant also cannot handle account-specific issues such as refunds, payment failures or address changes.

For responsible use, the assistant should show citations, refuse low-confidence answers, route sensitive cases to a human support agent, and log future failures for review. The safest next step is a human-supervised pilot for common FAQ questions only.
