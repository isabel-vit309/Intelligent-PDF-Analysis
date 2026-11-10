
import pymupdf


def extract_pdf_pages(pdf_bytes):
    """
    Extrai o texto de cada página de um arquivo PDF.

    Args:
        pdf_bytes: Conteúdo do PDF em bytes.

    Returns:
        Lista de dicionários contendo o número da página e seu texto.
    """
    pages = []

    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")

            if text.strip():
                pages.append({
                    "page": page_number,
                    "text": text.strip()
                })

    return pages


def chunk_pages(pages, chunk_size=220, overlap=45):
    """
    Divide o texto das páginas em blocos menores,
    mantendo uma sobreposição entre os blocos.

    Args:
        pages: Lista de páginas extraídas do PDF.
        chunk_size: Quantidade máxima de palavras por bloco.
        overlap: Quantidade de palavras repetidas entre blocos.

    Returns:
        Lista de blocos contendo texto e número da página.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size deve ser maior que zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap deve ser maior ou igual a zero e menor que chunk_size.")

    chunks = []

    for page in pages:
        words = page["text"].split()

        start = 0

        while start < len(words):
            end = start + chunk_size

            chunk_text = " ".join(words[start:end])

            if chunk_text.strip():
                chunks.append({
                    "text": chunk_text,
                    "page": page["page"]
                })

            start += chunk_size - overlap

    return chunks
