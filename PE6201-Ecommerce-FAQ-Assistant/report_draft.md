# PE6201 End-of-Course Project Report Draft

## AI Multilingual FAQ Assistant for Cross-Border E-commerce

### 1. Problem and significance

Cross-border e-commerce customers often ask simple support questions in different languages, but policy information can be scattered across return, shipping, customs and warranty pages. This creates slow, incomplete or inconsistent answers, especially when a customer cannot easily read the store's main support language. The project therefore builds a small multilingual FAQ assistant that helps customers find approved support information quickly while reducing the risk of unsupported answers.

### 2. Why AI and which kind

A fixed rule or keyword search can match obvious words such as "return" or "shipping", but it handles multilingual wording and paraphrase poorly. A pure foundation-model answer is also risky because it may invent a policy that is not in the store FAQ. I therefore chose a retrieval-grounded assistant: it first retrieves the most relevant FAQ record, then answers only from that record. In this prototype the answer layer is deterministic rather than a paid model call, because the first goal is to prove the retrieval and refusal behaviour before adding generation cost and hallucination risk.

### 3. Build vs buy trade-off

The project owns the FAQ data, retrieval logic, evaluation harness and demo interface. It rents nothing in the first version, so it runs without an API key and can be reproduced on another machine. A commercial chatbot platform would provide a nicer interface and stronger multilingual generation, but it would hide the retrieval logic and make cost harder to measure. A later version could rent a foundation model only for paraphrasing the grounded answer, while keeping retrieval, refusal rules and evaluation under project control.

### 4. Data and implementation

The prototype uses a small FAQ knowledge base with return, shipping, lost package, cancellation, customs, payment and warranty entries in English, Chinese and Spanish. The assistant tokenises the customer question, detects the likely language, scores FAQ entries by overlap and topic keywords, and returns the highest-scoring entry only if it passes a relevance threshold. If no entry is strong enough, it refuses to answer and asks the user to contact support. This design targets the main failure mode: giving confident answers that are not supported by the FAQ.

### 5. Evaluation and measured results

I built a 10-case evaluation harness. Each case specifies a customer question, the expected FAQ source and required answer terms. The harness runs every case, checks whether the retrieved source and answer content match, and records pass rate, approximate input tokens, output tokens, latency and estimated cost. The current version passed 10/10 cases. Average latency was 0.0002 seconds, average input was 24.1 estimated tokens, average output was 19.3 estimated tokens, and total estimated cost for the 10-case run was USD 0.000410. These figures are small because the current prototype uses local retrieval and template answers rather than a live model.

### 6. Risks, limitations and responsible use

The system should not be deployed as a final customer-service replacement. The FAQ set is small, the token estimate is approximate, and the multilingual coverage is limited. Retrieval can still fail if a customer uses unusual wording or asks a mixed-intent question. The assistant also cannot handle account-specific issues such as refunds, payment failures or address changes. For a real deployment, the system should show citations, refuse low-confidence answers, route sensitive cases to a human agent and log evaluation results over real customer questions. The safest next step is a human-supervised pilot for common FAQ questions only.
