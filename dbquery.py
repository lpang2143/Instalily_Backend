from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
import os

def get_index():
    pinecone_key = os.environ['PINECONE_KEY']
    if not pinecone_key:
        pinecone_key_file = open('pinecone_key.txt', mode='r')
        pinecone_key = pinecone_key_file.readline().strip()
    # print(pinecone_key)
    pc = Pinecone(api_key=pinecone_key)
    index = pc.Index('part-select')
    return index

def part_query(part_number:str, query: str):
    # print('We made it here')
    index = get_index()
    query_params = {}
    if part_number:
        query_params['part_number'] = {'$eq': part_number}

    embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")
    vector = embedding_model.embed_query(query)

    if query_params:
        response = index.query(
            vector=vector,
            top_k=10,
            filter=query_params,
            include_metadata=True
        )
    else:
        response = index.query(
            vector=vector,
            top_k=10,
            include_metadata=True
        )
        
    return response

def model_query(model_number:str, query: str):
    # print('We made it here')
    index = get_index()
    query_params = {}
    if model_number:
        query_params['model_number'] = {'$eq': model_number}

    embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")
    vector = embedding_model.embed_query(query)

    if query_params:
        response = index.query(
            vector=vector,
            top_k=10,
            filter=query_params,
            include_metadata=True
        )
    else:
        response = index.query(
            vector=vector,
            top_k=10,
            include_metadata=True
        )
        
    return response

def manufacturer_query(manufacturer:str, query: str):
    # print('We made it here')
    index = get_index()
    query_params = {}
    if manufacturer:
        print(f"{manufacturer}.txt")
        # Accidentally upserted manufacturers with .txt because they were at the end of the filename haha
        query_params['manufacturer'] = {'$eq': manufacturer}

    embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")
    vector = embedding_model.embed_query(query)

    if query_params:
        response = index.query(
            vector=vector,
            top_k=10,
            filter=query_params,
            include_metadata=True
        )
    else:
        response = index.query(
            vector=vector,
            top_k=10,
            include_metadata=True
        )
        
    return response

def general_query(query: str):
    # print('We made it here')
    index = get_index()

    embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")
    vector = embedding_model.embed_query(query)

    response = index.query(
        vector=vector,
        top_k=10,
        include_metadata=True
    )
        
    return response

if __name__ == '__main__':
    key_file = open('key.txt', mode='r')
    key = key_file.readline().strip()
    os.environ['OPENAI_API_KEY'] = key
    get_index()