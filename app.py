import streamlit as st

from rag.config import Settings
from rag.generation.answer_generator import source_label
from rag.pipeline import RagPipeline


SAMPLES = [
    "What does the report say about COVID-19 and life expectancy?",
    "As of what month and year are the Excel annex figures latest available?",
    "For Pakistan, what is the adolescent birth rate for ages 15–19 in the annex, and what is the data year?",
    "What does Figure 1.3 compare?",
]


@st.cache_resource
def get_rag() -> RagPipeline:
    return RagPipeline()


st.set_page_config(page_title="RAG", page_icon="📚")
st.title("WHO PDF + Excel RAG")
st.caption("Ask the report and its Excel annex. Answers include source numbers.")

if not Settings().chroma_dir.exists():
    st.warning("Index missing. Run `python -m rag.cli ingest` once, then refresh this page.")
    st.stop()

rag = get_rag()
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Try a question")
    sample_question = None
    for number, sample in enumerate(SAMPLES):
        if st.button(sample, key=f"sample_{number}"):
            sample_question = sample

    st.divider()
    agentic = st.toggle("Agentic search", value=False)
    st.caption("Agentic search lets Groq choose search terms. It makes one extra API call.")

    if st.button("Reload index"):
        get_rag.clear()
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["text"])
        if message.get("sources"):
            with st.expander("Sources"):
                for source in message["sources"]:
                    st.write(source)

typed_question = st.chat_input("Ask about the WHO report or Excel annex")
question = sample_question or typed_question

if question:
    st.session_state.messages.append({"role": "user", "text": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching and asking Groq..."):
            try:
                answer, documents = rag.ask_with_sources(question, agentic=agentic)
            except Exception as error:
                st.error(str(error))
                st.stop()

        st.write(answer)
        sources = [f"[{i}] {source_label(doc)}" for i, doc in enumerate(documents, 1)]
        with st.expander("Sources"):
            for source in sources:
                st.write(source)

    st.session_state.messages.append(
        {"role": "assistant", "text": answer, "sources": sources}
    )
    st.session_state.latest = (question, answer, documents)

if st.session_state.get("latest") and st.button("Evaluate last answer with RAGAS"):
    from eval.evaluator import RagasEvaluator

    question, answer, documents = st.session_state.latest
    with st.spinner("Checking whether the answer is supported by its sources..."):
        try:
            settings = Settings()
            evaluator = RagasEvaluator(settings.answer_model, settings.groq_api_key)
            score = evaluator.score(question, answer, documents)
            st.success(f"RAGAS faithfulness: {score:.2f} / 1.00")
        except Exception as error:
            st.error(str(error))
