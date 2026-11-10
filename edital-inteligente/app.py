import streamlit as st
from services.pdf_service import extract_pdf_pages, chunk_pages
from services.vector_service import index_document, search_document
from services.llm_service import answer_question

st.set_page_config(page_title="Edital Inteligente", page_icon="📄", layout="wide")
st.title("📄 Edital Inteligente")
st.caption("Assistente de consulta a editais com RAG, modelos locais e referências às páginas.")

with st.sidebar:
    st.header("Configuração")
    st.write("LLM: `qwen2.5:3b`")
    st.write("Embeddings: `embeddinggemma`")
    st.info("Os modelos são executados localmente pelo Ollama. Nenhuma API paga é necessária.")

uploaded_file = st.file_uploader("Envie um edital em PDF", type=["pdf"])

if uploaded_file:
    pdf_bytes = uploaded_file.getvalue()
    st.write(f"**Documento:** {uploaded_file.name} · **Tamanho:** {len(pdf_bytes) / 1024:.1f} KB")

    if st.button("Processar edital", type="primary"):
        with st.spinner("Extraindo e indexando o documento..."):
            pages = extract_pdf_pages(pdf_bytes)
            if not pages:
                st.error("Não foi possível extrair texto deste PDF. Ele pode ser digitalizado como imagem e precisar de OCR.")
            else:
                chunks = chunk_pages(pages)
                if not chunks:
                    st.error("Nenhum trecho de texto suficiente foi encontrado no documento.")
                else:
                    doc_id, count = index_document(
                        filename=uploaded_file.name,
                        pdf_bytes=pdf_bytes,
                        chunks=chunks,
                    )
                    st.session_state["doc_id"] = doc_id
                    st.session_state["doc_name"] = uploaded_file.name
                    st.success(f"Documento processado! {len(pages)} páginas com texto e {count} trechos indexados.")

if "doc_id" in st.session_state:
    st.divider()
    st.subheader(f"Pergunte sobre: {st.session_state['doc_name']}")
    question = st.text_input(
        "Sua pergunta",
        placeholder="Ex.: Qual é o prazo para envio das propostas?"
    )
    if st.button("Enviar pergunta", disabled=not question.strip()):
        with st.spinner("Localizando informações e elaborando a resposta..."):
            retrieved = search_document(st.session_state["doc_id"], question, n_results=5)
            if not retrieved:
                st.warning("Não encontrei trechos suficientes para responder. Tente reformular a pergunta.")
            else:
                response = answer_question(question, retrieved)
                st.markdown("### Resposta")
                st.write(response)
                st.markdown("### Trechos consultados")
                for item in retrieved:
                    with st.expander(f"Página {item['page']} · Relevância: {item['distance']:.3f}"):
                        st.write(item["text"])

st.divider()
st.caption("Protótipo acadêmico. As respostas devem ser conferidas no edital original e não substituem análise jurídica ou administrativa.")
