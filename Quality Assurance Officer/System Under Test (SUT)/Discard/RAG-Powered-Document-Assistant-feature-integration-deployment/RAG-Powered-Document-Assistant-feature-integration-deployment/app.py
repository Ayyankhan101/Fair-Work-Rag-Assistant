import streamlit as st
import json
import os

from scripts.rag_chain import load_vector_store, answer_question
from scripts.ingest import ingest_pdf


# ---------------------------------------------------
# Page Config
# ---------------------------------------------------

st.set_page_config(
    page_title="RAG Powered Document Assistant",
    page_icon="📄",
    layout="wide"
)



# ---------------------------------------------------
# CSS
# ---------------------------------------------------

st.markdown("""
<style>

.block-container{
    max-width:900px;
    padding-top:2rem;
}

h1{
    text-align:center;
}

.chat-title{
    text-align:center;
    color:#888;
    margin-bottom:25px;
    font-size:18px;
}

section[data-testid="stSidebar"]{
    background:#0E1117;
}

div[data-testid="stChatMessage"]{
    border-radius:15px;
}

.history-item{
    padding:10px;
    border-radius:8px;
    background:#262730;
    margin-bottom:8px;
    font-size:14px;
}

</style>

""", unsafe_allow_html=True)



# ---------------------------------------------------
# History
# ---------------------------------------------------

HISTORY_FILE = "chat_history.json"



def load_history():

    if os.path.exists(HISTORY_FILE):

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    return []



def save_history(history):

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )



# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.title(
    "📄 RAG Powered Document Assistant"
)


st.markdown(
"""
<div class='chat-title'>
Ask questions from uploaded documents using Retrieval-Augmented Generation (RAG)
</div>
""",
unsafe_allow_html=True
)



# ---------------------------------------------------
# Vector Store
# ---------------------------------------------------

@st.cache_resource

def get_vector_store():

    return load_vector_store()



vector_store = get_vector_store()



# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = load_history()



# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:


    # -----------------------------
    # PDF Upload
    # -----------------------------

    st.header("📄 Upload PDF")


    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"]
    )


    if uploaded_file:


        if st.button(
            "⚡ Process PDF",
            use_container_width=True
        ):


            with st.spinner(
                "Reading and indexing PDF..."
            ):


                ingest_pdf(
                    uploaded_file
                )


            st.success(
                "PDF processed successfully!"
            )


            st.cache_resource.clear()



    st.divider()



    # -----------------------------
    # History
    # -----------------------------

    st.header(
        "🕘 Search History"
    )


    if st.button(
        "🗑️ Clear History",
        use_container_width=True
    ):


        st.session_state.messages = []


        if os.path.exists(HISTORY_FILE):

            os.remove(HISTORY_FILE)


        st.rerun()



    st.divider()



    questions = [

        msg["content"]

        for msg in st.session_state.messages

        if msg["role"] == "user"

    ]



    if questions:


        for q in reversed(questions):

            st.markdown(
                f"""
                <div class="history-item">
                🔍 {q}
                </div>
                """,
                unsafe_allow_html=True
            )


    else:

        st.caption(
            "No searches yet."
        )



# ---------------------------------------------------
# Previous Messages
# ---------------------------------------------------

for message in st.session_state.messages:


    with st.chat_message(
        message["role"]
    ):


        st.markdown(
            message["content"]
        )


        if (
            message["role"]=="assistant"
            and "sources" in message
        ):


            with st.expander(
                "📚 Sources"
            ):


                for src in message["sources"]:

                    st.write(
                        f"📄 {src}"
                    )



# ---------------------------------------------------
# Chat Input
# ---------------------------------------------------

prompt = st.chat_input(
    "Ask a question about the documents..."
)



if prompt:


    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )


    save_history(
        st.session_state.messages
    )



    with st.chat_message(
        "user"
    ):

        st.markdown(
            prompt
        )



    with st.chat_message(
        "assistant"
    ):


        with st.spinner(
            "Searching documents..."
        ):


            result = answer_question(
                prompt,
                vector_store
            )



        st.markdown(
            result["answer"]
        )


        with st.expander(
            "📚 Sources",
            expanded=True
        ):


            for src in result["sources"]:

                st.write(
                    f"📄 {src}"
                )



    st.session_state.messages.append(

        {
            "role":"assistant",
            "content":result["answer"],
            "sources":result["sources"]
        }

    )


    save_history(
        st.session_state.messages
    )


    st.rerun()



# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.markdown("---")


st.caption(
    "❤️ Built with Streamlit • LangChain • FAISS • FastEmbed"
)