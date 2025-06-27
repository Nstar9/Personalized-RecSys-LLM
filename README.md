
# Personalized RecSys-LLM

> **A real-time, explainable movie recommendation system with A/B testing, LLM-powered onboarding, and public analytics dashboard. Built with FastAPI, Streamlit, and Pandas.**

---

## 🚀 Live Demo

* **Streamlit Dashboard:** [View Live](https://personalized-recsys-llm-fhvj5qghctzspy7qxvp8bj.streamlit.app/)
* **API (FastAPI, Render):** [Test Live](https://personalized-recsys-llm.onrender.com)
* **GitHub:** [View Repo](https://github.com/Nstar9/Personalized-RecSys-LLM)

---

## ⭐️ Why I Built This

As a technical product manager, I believe in building systems that are both **intelligent** and **transparent**.
This project solves a real business problem:
**How do you make personalized recommendations explainable, testable, and user-centric in real time?**

* **Bridges ML, product analytics, and UX**
* Inspired by product management interviews and real-world use cases at Microsoft, Google, etc.
* Shows how LLMs and cloud-native analytics can deliver explainable, A/B-tested recommendations at scale.

---

## 🧩 Features

* **Personalized Movie Recommendations API**
  Built with FastAPI; returns tailored movie suggestions for any user in real time.

* **A/B Testing of ML Models**
  Instantly compare different recommendation model versions (v1 vs v2) with live analytics and user feedback tracking.

* **GROQ/LLM-Powered User Onboarding**
  Converts free-form natural language (“I love sci-fi and comedy with strong female leads”) into actionable user profiles using LLMs (GROQ/LLM integration for robust, production-ready inference).

* **Explainable Recommendations (LLM-driven)**
  Every recommendation can be explained to the end-user using the same GROQ/LLM pipeline for full transparency (“why this movie for you?”).

* **Real-Time Feedback Logging**
  Users submit ‘like/dislike’ feedback on recommendations—captured instantly for model retraining and analytics.

* **Transparent, Live Analytics Dashboard**
  Streamlit dashboard visualizes A/B tests, user behavior, recommendation trends, and feedback in real time.

* **Cloud-Native, Production-Ready Deployment**

  * Streamlit Cloud (dashboard)
  * Render.com (API backend)
  * Public endpoints and self-service API docs

* **Plug-and-Play Data Pipelines**
  Pandas-based log processing and analytics; designed for easy extension to other domains (e.g., music, products, finance).

---

## 💡 Technical Highlights

* **FastAPI** for high-performance, async REST API serving
* **Streamlit** for live, beautiful analytics dashboards
* **GROQ/LLM integration** for:

  * Natural language onboarding → structured profiles
  * LLM-based recommendation explanations
* **Pandas** for all data processing, EDA, and analytics pipelines
* **A/B testing** baked into the rec API and analytics
* **Feedback loop** for user interactions and continuous improvement
* **Fully public cloud deployment:**

  * Render.com (API, with persistent storage)
  * Streamlit Cloud (dashboard, open acce
---

## 🗂️ Project Structure

```
├── dashboard.py         # Streamlit analytics dashboard
├── main.py              # FastAPI backend (recommend, onboard, feedback, explain)
├── data/
│   ├── u.item           # Movie metadata (MovieLens)
│   ├── ab_log.csv       # API call logs for A/B test
│   ├── feedback_log.csv # User feedback log
│   ├── explanation_log.csv # LLM explanations log
├── requirements.txt
├── README.md
```

---

## 🏄 How To Run & Test

### 1. **Local Setup**

```bash
git clone https://github.com/Nstar9/Personalized-RecSys-LLM.git
cd Personalized-RecSys-LLM
pip install -r requirements.txt
```

* **Run API:**
  `uvicorn main:app --reload`
* **Run Dashboard:**
  `streamlit run dashboard.py`
* **Open API Docs:**
  Go to `http://localhost:8000/docs` in your browser

---

### 2. **Live Demos**

* **Dashboard:**
  [https://personalized-recsys-llm-fhvj5qghctzspy7qxvp8bj.streamlit.app/](https://personalized-recsys-llm-fhvj5qghctzspy7qxvp8bj.streamlit.app/)
* **API:**
  [https://personalized-recsys-llm.onrender.com](https://personalized-recsys-llm.onrender.com)

---

## 🖼️ Screenshots

> **Drop your key screenshots here**
>
> * Main Dashboard (A/B test, Recommendations)
> * ![Streamlit Dashboard](dashboard.png)
> * API Docs (Swagger UI)
> * Onboarding/Feedback endpoints
> * Example API responses
>   *Screenshots show actual working app and endpoints!*

---

## 📊 Example Usage

### **Get Recommendations**

```http
GET /recommend?user_id=1
```

### **Submit Feedback**

```json
POST /feedback
{
  "user_id": 1,
  "movie_id": 626,
  "feedback": "Like"
}
```

### **Onboard New User (LLM-powered)**

```json
POST /onboard
{
  "text": "I love sci-fi and comedy movies with strong female leads."
}
```

### **Get Explanation for a Recommendation**

```http
GET /explain?user_id=10&movie_id=1122
```

---

## 📈 Analytics Dashboard Features

* **A/B Test Results**
  Compare usage and impact for different rec models.
* **Sample Recommendations**
  View what’s being recommended live.
* **Top Movies**
  See most popular recommendations.
* **Feedback Tracking**
  User ‘like/dislike’ stats.
* **Live Usage Trends**
  API call stats by hour/day.
* **All data is real and up-to-date** (see screenshots).

---
## 🙋 About Me

I’m Niraj Patil, a technical product manager with deep hands-on skills in ML, cloud, analytics, and product strategy.

> *Looking for roles that combine product, data, and engineering at top-tier tech companies!*

---

## 📬 Contact

* [LinkedIn](https://www.linkedin.com/in/nirajpatil21/)
* [GitHub](https://github.com/Nstar9/)

---


