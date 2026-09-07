from sentence_transformers import SentenceTransformer 
import faiss 
import numpy as np 
import pandas as pd
import sys
import os
import json
import mysql.connector 
from dotenv import load_dotenv
import time
pd.reset_option("display.max_colwidth")

class SemanticSearcher: 
    def __init__(self): 
        self.model = SentenceTransformer('all-MiniLM-L6-v2') 
        self.index = None 
        self.listings = None 
    def build_index(self, remarks_list): 
        print(f"Encoding {len(remarks_list)} listings...") 
        embeddings = self.model.encode(remarks_list) 
        # Build FAISS index 
        dim = embeddings.shape[1] 
        self.index = faiss.IndexFlatIP(dim)  # Inner product for cosine sim 
        faiss.normalize_L2(embeddings) 
        self.index.add(embeddings) 
        self.listings = remarks_list 
    def load_index(self, index_path, remarks_list):
        self.index = faiss.read_index(index_path)
        self.listings = remarks_list
    def search(self, query, top_k=10): 
        query_emb = self.model.encode([query]) 
        faiss.normalize_L2(query_emb) 

        scores, indices = self.index.search(query_emb, top_k) 

        results = [
            (self.listings[i], float(scores[0][j])) 
            for j, i in enumerate(indices[0])] 
        return results 
    def search_texts(self, query, texts, top_k=10):
        if not texts:
            return []

        embeddings = self.model.encode(texts)
        faiss.normalize_L2(embeddings)

        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)

        query_emb = self.model.encode([query])
        faiss.normalize_L2(query_emb)

        scores, indices = index.search(query_emb, min(top_k, len(texts)))

        results = [
            (i, float(scores[0][j]))
            for j, i in enumerate(indices[0])
        ]

        return results
    
    def search_indices(self, query, top_k=50):
        query_emb = self.model.encode([query])
        faiss.normalize_L2(query_emb)

        scores, indices = self.index.search(
            query_emb,
            min(top_k, len(self.listings))
        )

        return [
            (int(indices[0][j]), float(scores[0][j]))
            for j in range(len(indices[0]))
        ]
