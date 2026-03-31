# 🍷 RAG-Based Wine Recommendation System

A smart wine recommendation system powered by **Retrieval-Augmented Generation (RAG)** using vector search and LLMs.

---

## 🚀 Features

- 🔍 Semantic search using embeddings
- 🧠 RAG-based recommendation (retrieval + generation)
- ⚡ Fast similarity search with Qdrant
- 🤖 LLM-generated personalized suggestions
- 🎨 Streamlit UI with modern design

---

## 🧠 What is RAG?

**Retrieval-Augmented Generation (RAG)** is a technique that improves LLM responses by combining:

1. **Retrieval** → Fetch relevant data from a database  
2. **Generation** → Use LLM to generate response based on retrieved data  

### In this project:

- User enters wine preference  
- System retrieves similar wines from vector DB  
- LLM generates a final recommendation using those wines  

---

## 🏗️ Tech Stack

- **Frontend:** Streamlit  
- **Vector DB:** Qdrant  
- **Embeddings:** Sentence Transformers
- **LLM API:** OpenRouter
- **Backend:** Python  

---

## 📂 Project Structure
wine-recommendation-rag/
│── app.py 
│── utils.py 
│── requirements.txt 
│── wine-ratings.csv 
│── README.md

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/wine-recommendation-rag.git
cd wine-recommendation-rag
pip install -r requirements.txt
```

🔑 Environment Setup

Create a .env file in the project root and add your API key:
``` OPENROUTER_API_KEY=your_api_key_here ```

Install dotenv:
``` pip install python-dotenv```

▶️ Run the App
``` streamlit run app.py ```

🧪 Example Query
Suggest a bold red wine with dark fruit flavors and spicy notes

---

## 📌 Future Improvements
- Add filters (country, price, variety)
- Deploy on cloud
- Add user feedback system

---

## 👩‍💻 Author

Anshika Agrawal
