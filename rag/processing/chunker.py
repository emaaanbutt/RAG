from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  
        chunk_overlap=150, 
    )

    chunked_docs = []

    for doc in documents:
        chunks = text_splitter.split_text(doc["text"])

        for chunk in chunks:
            chunked_docs.append({"text": chunk, "metadata": doc["metadata"]})

    return chunked_docs