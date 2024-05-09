from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import pickle
import faiss
import numpy as np
chunks_embeddings = []
import pandas as pd 

app = Flask(__name__)

model_name = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

#IF pickle_file not found RUN resume_model.ipynb notebook by deleting the 
with open("pickle_file", 'rb') as f:
    loaded_data = pickle.load(f)

chunks_embeddings=[]

def initialize_chunks_embeddings():
    global chunks_embeddings
    #******** Load your DataFrame (df) ******
    df = pd.read_csv("jobs.csv")  # Replace "your_dataframe.csv" with your DataFrame file path
    df["result"]=df["company_id"]+df["job_name"]+df["taglist"]+df["location"]+df["three_reasons"]+df["description"]
    for i in range(len(df)):
        if isinstance(df['result'][i], str):
            # Process only if the element is a string
            text = df["result"][i]
            embedding = model.encode(text)
            chunks_embeddings.append((text, embedding))
        else:
            # Skip if the element is not a string
            continue

# Initialize chunks_embeddings when the Flask app starts
initialize_chunks_embeddings()

#  ****API_KEY****  #
api_key = "AIzaSyAuoggTUpQqaXsnGgp8Rd-U6NbXAyM3AIk"
# Configure GenerativeAI
genai.configure(api_key=api_key)
genmodel = genai.GenerativeModel('gemini-pro')


# Define your answer function
def answer(text):
    query_embedding = model.encode(text)
    query_embedding = np.array([query_embedding]).astype('float32')
    k = 10
    D, I = loaded_data.search(query_embedding, k)
    retrieved_list = [chunks_embeddings[i][0] for i in I[0]]
    texts = []
    for text in retrieved_list:
        texts.append(text)
    # response = genmodel.generate_content("find the name of the company, job, description, and location for each item in the list of individually {text} ".format(text=text))
    #GIVE YOUR SUITABLE PROMPT
    prompt = "Given the following text: '{texts}', please generate a json file of dictionary with keys 'company', 'job_title', 'description', and 'location'. The generated content should include the name of the company, job title, job description, and location associated with the provided text."
    response = genmodel.generate_content(prompt.format(texts=texts))
    response_text = response.text
    start_index = response_text.find("{")
    end_index = response_text.rfind("}") + 1

    # Extract the JSON content and remove surrounding triple backticks
    json_content = response_text[start_index:end_index].strip().replace('```', '')
    return json_content


# Define your Flask route
@app.route('/getDetails', methods=['GET', 'POST'])
def getJobDetails():
    if request.method == 'POST':
        data = request.get_json()
        print(data)

        text = data.get('text', '')
        print(text)

        response = answer(text)
        # print(response)

        return response

if __name__ == '__main__':
    app.run(app.run(host='0.0.0.0', port=80))
