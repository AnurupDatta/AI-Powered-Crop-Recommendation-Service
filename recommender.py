import os
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import cassio
from langchain.vectorstores.cassandra import Cassandra
from langchain.embeddings import HuggingFaceBgeEmbeddings

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_CROP_API")
ASTRA_DB_ID = os.getenv("ASTRA_DB_CROP_ID")

# 1. Load the CSV
df = pd.read_csv("Crop_recommendation.csv")

# 2. Initialize Astra DB connection
cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)

# 3. Create embedding model (using Hugging Face)
embedding = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 4. Create Cassandra vector store
astra_vector_store = Cassandra(
    embedding=embedding,
    table_name="crop_vectors",
    session=None,  # CassIO manages the session
    keyspace=None, # CassIO manages the keyspace
)

# 5. Prepare crop strings for embedding and storage
crop_strings = df.apply(
    lambda row: f"N {row['N']} P {row['P']} K {row['K']} temperature {row['temperature']} humidity {row['humidity']} ph {row['ph']} rainfall {row['rainfall']} label {row['label']}",
    axis=1
).tolist()

# 6. Store crop embeddings in Astra DB (only needs to be done once; skip if already stored)
# You may want to comment this out after the first run to avoid duplicate entries
astra_vector_store.add_texts(crop_strings)

# 7. Initialize Groq LLM
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"  # Use your preferred Groq model
)

def recommend_crops(temperature: float, humidity: float, moisture: float, k: int = 4):
    """
    Recommend top k crops and provide an explanation using Groq LLM.
    """
    # Create input string for embedding
    input_str = f"humidity {humidity} moisture {moisture} temperature {temperature}"

    # Query Astra DB for top k similar crops
    results = astra_vector_store.similarity_search(input_str, k=k)
    top_crops = [doc.page_content.split("label ")[-1] for doc in results]

    # Prepare prompt for Groq
    crop_list = ", ".join(top_crops)
    prompt = (
        f"Given the environmental conditions: humidity {humidity}%, "
        f"moisture {moisture}%, temperature {temperature}°C, "
        f"the top {k} suitable crops are: {crop_list}. "
        "Explain why these crops are suitable."
    )

    # Get Groq LLM response
    response = llm.invoke(prompt)

    return {
        "crops": top_crops,
        "explanation": response
    }