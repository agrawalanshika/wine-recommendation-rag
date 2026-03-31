import pandas as pd
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

print("📦 Loading embedding model...")

encoder = SentenceTransformer('all-MiniLM-L6-v2')

print("✅ Model loaded!")

qdrant = QdrantClient(path="./qdrant_data")


df = pd.read_csv("wine-ratings.csv")
df = df[df['variety'].notna()]
df = df[df['notes'].notna()]
df = df.drop_duplicates()
df = df.reset_index(drop=True)
data = df.to_dict('records')

if "top_wines" not in [c.name for c in qdrant.get_collections().collections]:
    qdrant.create_collection(
        collection_name="top_wines",
        vectors_config=models.VectorParams(
            size=encoder.get_sentence_embedding_dimension(),
            distance=models.Distance.COSINE
        )
    )

def upload_data():
    print("📤 Uploading data to Qdrant...")

    points = []
    for idx, doc in enumerate(data):
        vector = encoder.encode(
            f"{doc['variety']} wine from {doc.get('country','')}. {doc['notes']}"
        ).tolist()

        points.append(
            models.PointStruct(
                id=idx,
                vector=vector,
                payload=doc
            )
        )

    qdrant.upload_points(
        collection_name="top_wines",
        points=points
    )

    print("✅ Data upload complete!")

def search_wines(query, country=None):
    filter_condition = None

    if country:
        filter_condition = models.Filter(
            must=[
                models.FieldCondition(
                    key="country",
                    match=models.MatchValue(value=country)
                )
            ]
        )

    return qdrant.query_points(
        collection_name="top_wines",
        query=encoder.encode(query).tolist(),
        query_filter=filter_condition,
        limit=3
    )