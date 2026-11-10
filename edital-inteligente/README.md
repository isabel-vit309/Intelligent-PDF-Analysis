# Edital Inteligente

Protótipo acadêmico de assistente para consulta a editais em PDF usando RAG e modelos locais.

## Tecnologias

- Python
- Streamlit
- PyMuPDF
- Ollama
- Qwen 2.5 3B (LLM)
- EmbeddingGemma (embeddings)
- ChromaDB (banco vetorial)

## Pré-requisitos

- Python 3.10 ou superior
- Ollama instalado
- Memória RAM suficiente para executar os modelos localmente

## 1. Instalar e baixar os modelos

Instale o Ollama em https://ollama.com/ e execute no terminal:

```powershell
ollama pull qwen2.5:3b
ollama pull embeddinggemma
```

## 2. Preparar o ambiente Python (Windows PowerShell)

Na pasta do projeto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Se o PowerShell bloquear a ativação, consulte a política de execução do seu ambiente ou use o terminal CMD:

```cmd
.venv\Scripts\activate.bat
```

## 3. Executar

Garanta que o Ollama esteja em execução e rode:

```powershell
streamlit run app.py
```

O navegador abrirá a interface local.

## Como funciona

1. O usuário envia um edital em PDF.
2. PyMuPDF extrai o texto página por página.
3. O texto é dividido em trechos com sobreposição.
4. EmbeddingGemma gera embeddings localmente.
5. ChromaDB armazena os vetores e metadados de página.
6. A pergunta do usuário também é convertida em embedding.
7. ChromaDB recupera os trechos semanticamente mais próximos.
8. Qwen 2.5 gera uma resposta baseada nos trechos recuperados.
9. A interface apresenta a resposta e os trechos consultados.

## Limitações conhecidas da primeira versão

- PDFs digitalizados como imagem não são processados; será necessário adicionar OCR.
- O protótipo trabalha com um documento selecionado por vez.
- A qualidade depende da extração de texto e dos trechos recuperados.
- A resposta da LLM deve ser conferida no edital original.
- O modelo local pode ser lento em computadores com pouca memória ou sem aceleração por GPU.

## Observação acadêmica

A implementação é um protótipo de apoio à consulta documental. Não substitui a leitura integral do edital nem a análise jurídica ou administrativa.
