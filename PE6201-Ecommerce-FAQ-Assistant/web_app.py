from pathlib import Path

import streamlit as st

from src.assistant import answer_question
from src.retrieval import load_faq


ROOT = Path(__file__).parent
FAQ_PATH = ROOT / "data" / "faq.json"


@st.cache_data
def cached_faq():
    return load_faq(FAQ_PATH)


st.set_page_config(page_title="Multilingual FAQ Assistant", page_icon="🌐")

st.title("AI Multilingual FAQ Assistant")
st.caption("Cross-border e-commerce support demo for PE6201")

st.write(
    "Ask a customer-support question in English, Chinese or Spanish. "
    "The assistant retrieves an approved FAQ record, answers from that evidence, "
    "and refuses when the FAQ does not support an answer."
)

examples = [
    "Can I return an item after 14 days?",
    "我的包裹丢了怎么办？",
    "¿Puedo cancelar mi pedido?",
    "Can you recommend the best laptop for gaming?",
]

query = st.text_input("Customer question", value=examples[0])

with st.expander("Try example questions"):
    for example in examples:
        st.code(example)

if st.button("Answer question", type="primary"):
    response = answer_question(query, cached_faq())
    st.subheader("Answer")
    st.write(response.answer)

    st.subheader("Evidence")
    if response.source_id:
        st.write(f"Source ID: `{response.source_id}`")
        st.write(f"Source: `{response.source_name}`")
        st.write(f"Retrieval confidence: `{response.confidence:.2f}`")
    else:
        st.warning("No sufficiently relevant FAQ record was found.")

    st.subheader("Run metrics")
    st.table(
        {
            "Metric": ["Input tokens", "Output tokens", "Latency", "Estimated cost"],
            "Value": [
                response.metrics.input_tokens,
                response.metrics.output_tokens,
                f"{response.metrics.latency_seconds:.4f}s",
                f"${response.metrics.estimated_cost_usd:.8f}",
            ],
        }
    )
