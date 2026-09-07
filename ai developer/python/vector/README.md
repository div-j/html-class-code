
# Vector Similarity Search with FAISS

## Project Overview
This project demonstrates how to convert a collection of text documents into vector embeddings and build a FAISS index for efficient similarity search.  
It shows the complete pipeline from raw text → embeddings → searchable index → natural language retrieval.

## Features
- Prepare a document corpus
- Generate dense vector embeddings using `sentence-transformers`
- Build a FAISS index (L2 / Euclidean distance)
- Perform semantic search with natural language queries
- Retrieve the most relevant documents ranked by similarity

## Project Structure
```
vector/
├── project.ipynb          # Main notebook containing the full pipeline
└── README.md              # This file
```

## Requirements
- Python 3.8+
- Libraries:
  - `sentence-transformers`
  - `faiss-cpu` (or `faiss-gpu` if you have a GPU)
  - `numpy`

Install the dependencies with:

```bash
pip install sentence-transformers faiss-cpu numpy
```

## How to Run
1. Open the notebook:
   ```bash
   jupyter notebook vector/project.ipynb
   ```
2. Run all cells in order.
3. Change the query in the last section to test different searches.

## Pipeline Steps
1. **Corpus Preparation**  
   A small set of documents about AI, machine learning, and related topics is defined.

2. **Embedding Generation**  
   The model `all-MiniLM-L6-v2` converts each document into a 384-dimensional vector.

3. **FAISS Index Construction**  
   An `IndexFlatL2` index is created and populated with the document embeddings.

4. **Similarity Search**  
   A natural language query is embedded and used to retrieve the top-k most similar documents.

## Example
**Query:**  
`"How can I use AI in industry?"`

**Expected Top Result:**  
`"Artificial Intelligence is transforming industries across the world."`

## Notes
- The index uses L2 (Euclidean) distance. Lower distance = higher similarity.
- The notebook is self-contained and ready for demonstration or submission.
- You can easily replace the sample corpus with your own documents.


---

### How to use it
1. Create a file named `README.md` inside the `vector/` folder (or next to `project.ipynb`).
2. Paste the content above.
3. Save it.
