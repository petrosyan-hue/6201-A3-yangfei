# Demo Script

## Opening

This is my PE6201 End-of-Course Project: an AI multilingual FAQ assistant for cross-border e-commerce. The problem is that customers ask support questions in different languages, while return, shipping and customs information may be scattered across several FAQ pages.

## System demo

The user enters a customer question. For example, "Can I return an item after 14 days?" The system retrieves the matching FAQ record and answers from that evidence. It also shows the source ID, retrieval confidence, estimated tokens, latency and estimated cost.

Now I test a Chinese question: "我的包裹丢了怎么办？" The assistant retrieves the Chinese lost-package FAQ and asks the customer to contact support with the order number and tracking number.

Finally, I test a question outside the FAQ: "Can you recommend the best laptop for gaming?" The assistant refuses to guess because no relevant FAQ record supports the answer.

## Evaluation

The evaluation harness contains 10 test cases. Each case has a question, an expected FAQ source and required answer terms. The current prototype passes 10 out of 10 cases. It also records average latency, estimated input tokens, estimated output tokens and estimated cost.

## Limitations

This is a first version, not a production chatbot. The FAQ set is small and the answer layer is deterministic. A future version could add a foundation model for more natural wording, but only after keeping retrieval citations, low-confidence refusal and human escalation.
