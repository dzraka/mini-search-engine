import pandas as pd

from flask import Flask, request, jsonify, render_template
from search_engine import build_inverted_index, calculated_tfidf, search

app = Flask(__name__)

# Load CSV dengan parsing manual untuk preserve semua data
komentar_list = []
with open('vaksin_campak.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines[1:]:
        line = line.strip()
        if line:
            komentar_list.append(line)

# Transformasi ke DataFrame
df_raw = pd.DataFrame({
    'id_str': range(1, len(komentar_list) + 1),
    'full_text': komentar_list,
    'komentar': komentar_list
})
total_docs = len(df_raw)

doc_lookup = df_raw.set_index(df_raw['id_str'].astype(str)).to_dict(orient='index')

inverted_index = build_inverted_index(df_raw)
tfidf_index, idf_dict, doc_magnitudes = calculated_tfidf(inverted_index, total_docs)

@app.route('/')
def home():
    all_docs = df_raw[['id_str', 'full_text']].to_dict(orient='records')
    return render_template('index.html', documents=all_docs, total_docs=len(all_docs))

@app.route('/get-all-docs', methods=['GET'])
def get_all_docs():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    all_docs = df_raw[['id_str', 'full_text']].to_dict(orient='records')
    total = len(all_docs)
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_docs = all_docs[start:end]
    total_pages = (total + per_page - 1) // per_page
    
    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "results": paginated_docs
    })

@app.route('/search', methods=['GET'])
def handle_search():
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 10

    if not query:
        return jsonify({
            "query": query,
            "page": page,
            "per_page": per_page,
            "total": 0,
            "total_pages": 0,
            "results": []
        })

    results = search(query, tfidf_index, idf_dict, doc_magnitudes, doc_lookup)
    total = len(results)
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_results = results[start:end]
    total_pages = (total + per_page - 1) // per_page

    return jsonify({
        "query": query,
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "results": paginated_results
    })

if __name__ == '__main__':
    app.run(debug=True)