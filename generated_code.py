# Import required libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import requests

# Create a FastAPI application
app = FastAPI()

# Define a Pydantic model for API requests and responses
class GitHubRequest(BaseModel):
    access_token: str
    repository: str

class GitHubResponse(BaseModel):
    data: str
    status: str

# Define the API endpoint for getting data from GitHub
@app.post("/get_data")
async def get_data(request: GitHubRequest):
    """
    Retrieves data from GitHub API.

    Args:
        access_token: A valid GitHub access token.
        repository: The GitHub repository to retrieve data from.

    Returns:
        A dictionary containing the retrieved data and status.
    """

    try:
        # Replace with your GitHub API endpoint URL
        url = f"https://api.github.com/repos/{request.repository}"

        # Use the access token in the request headers
        headers = {
            "Authorization": f"Bearer {request.access_token}",
            "Content-Type": "application/json"
        }

        # Send a GET request to the GitHub API
        response = requests.get(url, headers=headers)

        # Check if the response was successful
        if response.status_code == 200:
            data = response.json()
            return {"data": data, "status": "success"}
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    except Exception as e:
        # Catch any exceptions and return an error message
        return {"data": str(e), "status": "error"}

# Run the API using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)