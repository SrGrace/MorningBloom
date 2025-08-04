import os
from dotenv import load_dotenv
load_dotenv(override=True)

WATSONX_API_KEY = os.getenv("API_KEY")
WATSONX_PROJECT_ID = os.getenv("PROJECT_ID")
WATSONX_CLOUD_URL = os.getenv("IBM_CLOUD_URL")
# VECTORDB_URI = os.getenv("VECTORDB_URI")

def watsonx_enabled():
    # return all([WATSONX_API_KEY, WATSONX_PROJECT_ID, WATSONX_ENDPOINT])
    wx_credentials = {
        "url": WATSONX_CLOUD_URL,
        "apikey": WATSONX_API_KEY,
        "project_id": WATSONX_PROJECT_ID,
    }
    return wx_credentials
