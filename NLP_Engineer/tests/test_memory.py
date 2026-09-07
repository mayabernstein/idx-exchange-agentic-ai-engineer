import os
import psutil
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss


def memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024**2


print(f"Starting memory: {memory_usage():.1f} MB")


print("\nLoading SentenceTransformer...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print(f"After model: {memory_usage():.1f} MB")


print("\nLoading CSV...")
listings_df = pd.read_csv(
    "../data/processed/cleaned_listing_full.csv",
    usecols=[
        "L_ListingID",
        "L_Address",
        "L_City",
        "beds",
        "baths",
        "price",
        "sqft",
        "cleaned_remarks",
        "L_Zip"
    ],
    dtype={
        "beds": "float32",
        "baths": "float32",
        "price": "int32",
        "sqft": "float32"
    }
)

listings_df = listings_df.reset_index(drop=True)
print(f"After CSV: {memory_usage():.1f} MB")


print("\nCreating remarks list...")
remarks_list = listings_df["cleaned_remarks"].fillna("").tolist()
print(f"After remarks list: {memory_usage():.1f} MB")


print("\nLoading FAISS index...")
index = faiss.read_index("../data/processed/listing_index_full.faiss")
print(f"After FAISS index: {memory_usage():.1f} MB")