import ollama

LLM_MODEL = "qwen2.5:3b"


def answer_question(question: str, retrieved_chunks: list[dict]) -> str:
    """Responde somente com base nos trechos recuperados do edital."""
    context_parts = []
    for item in retrieved_chunks:
        context_parts.append(
            f"[Página {item['page']}]\n{item['text']}"
        )
    context = "\n\n---\n\n".join(context_parts)

    system_prompt = """
Você é o Edital Inteligente, um assistente de consulta a editais públicos.
Responda em português brasileiro, de forma clara e objetiva.
Use exclusivamente as informações presentes no CONTEXTO fornecido.
Não invente datas, valores, requisitos, documentos ou cláusulas.
Se o contexto não contiver informação suficiente, diga explicitamente:
"Não encontrei essa informação nos trechos recuperados do edital."
Sempre indique as páginas que sustentam a resposta, usando o formato (página X).
Diferencie uma informação explícita de uma interpretação.
Não trate sua resposta como aconselhamento jurídico.
""".strip()

    user_prompt = f"""
CONTEXTO DO EDITAL:
{context}

PERGUNTA:
{question}

Responda com base exclusivamente no contexto acima e indique as páginas utilizadas.
""".strip()

    result = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        options={"temperature": 0.1},
    )
    return result["message"]["content"]
