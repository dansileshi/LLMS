import os
from llama_index import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers import PDFReader

def get_index(data, index_name):
    index = None

    if not os.path.exists(index_name):
        print("burilding index:", index_name)
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir = index_name)
    else:
        index = load_index_from_storge(
            StorageContext.from_defaults(persist_dir = index_name)
        )

    return index

pdf_path = os.path.join("data", "United_Kingdom.pdf")
UK_pdf = PDFReader().load_data(file = pdf_path)

UK_index =  get_index(UK_pdf, "UK_index")
UK_engine = UK_index.as_query_engine()




