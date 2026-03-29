from fastapi import FastAPI
from pydantic import BaseModel
from recommender import recommend_crops

app = FastAPI()

class CropRecommendationRequest(BaseModel):
    temperature: float
    humidity: float
    moisture: float

@app.post("/recommend_crops")
def recommend_crops_endpoint(request: CropRecommendationRequest):
    result = recommend_crops(request.temperature, request.humidity, request.moisture)
    return result