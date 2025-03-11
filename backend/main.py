import openai
import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Load API keys from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PRReviewRequest(BaseModel):
    repo_owner: str
    repo_name: str
    pr_number: int

def get_pr_diff(repo_owner, repo_name, pr_number):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        pr_data = response.json()
        diff_url = pr_data.get("diff_url")
        return diff_url, pr_data.get("html_url")
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch PR diff")

def analyze_code_with_ai(code_diff):
    openai.api_key = OPENAI_API_KEY
    prompt = f"Review the following code and provide suggestions for improvements:\n{code_diff}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a code review assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def post_github_comment(repo_owner, repo_name, pr_number, comment):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments"
    payload = json.dumps({"body": comment})
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail="Failed to post comment on PR")

@app.post("/review_pr")
def review_pull_request(request: PRReviewRequest):
    try:
        diff_url, pr_html_url = get_pr_diff(request.repo_owner, request.repo_name, request.pr_number)
        diff_response = requests.get(diff_url)
        if diff_response.status_code == 200:
            review_comments = analyze_code_with_ai(diff_response.text)
            post_github_comment(request.repo_owner, request.repo_name, request.pr_number, review_comments)
            return {"review": review_comments, "pr_url": pr_html_url}
        else:
            raise HTTPException(status_code=diff_response.status_code, detail="Failed to fetch PR diff content")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
