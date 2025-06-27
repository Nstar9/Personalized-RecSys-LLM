from fastapi import FastAPI, Query
import pandas as pd
import random
import csv
import os
import re
from datetime import datetime
from pydantic import BaseModel 
import requests

app = FastAPI()

# Load MovieLens data
ratings = pd.read_csv(
    "data/u.data",
    sep="\t",
    names=["user_id", "movie_id", "rating", "timestamp"]
)
movies = pd.read_csv(
    "data/u.item",
    sep="|",
    encoding="latin-1",
    names=["movie_id", "title"] + [f"junk{i}" for i in range(22)],
    usecols=[0, 1]
)
users = pd.read_csv(
    "data/u.user",
    sep="|",
    names=["user_id", "age", "gender", "occupation", "zip_code"]
)

@app.get("/")
def read_root():
    return {"status": "API is working"}

@app.get("/recommend")
def recommend(user_id: int = Query(..., description="User ID")):
    model_version = random.choice(['v1', 'v2'])
    user_rated = ratings[ratings.user_id == user_id].movie_id.tolist()
    unrated_movies = movies[~movies.movie_id.isin(user_rated)]
    
    if unrated_movies.empty:
        top_movies = movies.sample(n=5, random_state=42)
    else:
        if model_version == "v1":
            avg_ratings = ratings.groupby("movie_id").rating.mean().reset_index()
            unrated_with_ratings = unrated_movies.merge(avg_ratings, on="movie_id", how="left")
            top_movies = unrated_with_ratings.sort_values(by="rating", ascending=False).head(5)
        else:
            top_movies = unrated_movies.sample(n=min(5, len(unrated_movies)), random_state=42)

    recs = [
        {"movie_id": int(row.movie_id), "title": row.title}
        for _, row in top_movies.iterrows()
    ]

    # === LOGGING TO CSV ===
    log_file = "ab_log.csv"
    log_exists = os.path.isfile(log_file)
    with open(log_file, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not log_exists:
            writer.writerow(["timestamp", "user_id", "model_version", "recommendations"])
        writer.writerow([
            datetime.now().isoformat(), user_id, model_version,
            ";".join([str(rec["movie_id"]) for rec in recs])
        ])
    # ======================

    return {
        "user_id": user_id,
        "model_version": model_version,
        "recommendations": recs
    }

def get_llm_explanation(prompt):
    api_key = os.getenv("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 60,
        "temperature": 0.7
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return (
                f"Because you enjoyed movies like ... we think you'll love this one! (LLM fallback: Groq error: {response.text})"
            )
    except Exception as e:
        return (
            f"Because you enjoyed movies like ... we think you'll love this one! (LLM fallback: Exception: {str(e)})"
        )

@app.get("/explain")
def explain(user_id: int, movie_id: int):
    # Get user history (movies with rating >= 4)
    user_history = ratings[(ratings.user_id == user_id) & (ratings.rating >= 4)]
    recent_titles = movies[movies.movie_id.isin(user_history.movie_id)]['title'].tolist()[:5]

    # Get movie title
    movie_title = movies[movies.movie_id == movie_id]['title'].values[0]

    # Build prompt
    prompt = (
        f"User recently liked: {', '.join(recent_titles)}.\n"
        f"Recommended movie: {movie_title}.\n"
        "Write a one-line, human explanation for why this recommendation makes sense."
    )

    explanation = get_llm_explanation(prompt)

    # === LOG EXPLANATION TO CSV ===
    expl_log = "explanation_log.csv"
    log_exists = os.path.isfile(expl_log)
    with open(expl_log, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not log_exists:
            writer.writerow(["timestamp", "user_id", "movie_id", "explanation"])
        writer.writerow([
            datetime.now().isoformat(), user_id, movie_id, explanation
        ])
    # ==============================

    return {
        "user_id": user_id,
        "movie_id": movie_id,
        "explanation": explanation
    }

class OnboardRequest(BaseModel):
    text: str

@app.post("/onboard")
def onboard(req: OnboardRequest):
    text = req.text
    prompt = (
        f"A new user says: '{text}'. "
        "Extract their key interests and suggest 3-5 movie genres or tags for a recommendation system. "
        "Reply as a Python list of strings, and nothing else."
    )
    interests = get_llm_explanation(prompt)
    # Regex to extract the first Python list found in the output
    matches = re.findall(r"\[.*?\]", interests, re.DOTALL)
    if matches:
        try:
            interests_list = eval(matches[0])
            if not isinstance(interests_list, list):
                interests_list = [interests]
        except Exception:
            interests_list = [interests]
    else:
        interests_list = [interests]
    return {
        "input_text": text,
        "interests": interests_list
    }


class FeedbackRequest(BaseModel):
    user_id: int
    movie_id: int
    feedback: str  # e.g. "like", "dislike", "neutral", "clicked"

@app.post("/feedback")
def feedback(req: FeedbackRequest):
    log_file = "feedback_log.csv"
    log_exists = os.path.isfile(log_file)
    with open(log_file, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not log_exists:
            writer.writerow(["timestamp", "user_id", "movie_id", "feedback"])
        writer.writerow([datetime.now().isoformat(), req.user_id, req.movie_id, req.feedback])
    return {"status": "feedback recorded"}
