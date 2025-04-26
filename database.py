from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://ealmonrode:Kalafra@cluster0.s5u716e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" 

client = AsyncIOMotorClient(MONGO_URL)
db = client.quicktasks
