import math, re

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()

sw_sastrawi = set(StopWordRemoverFactory().get_stop_words())

def text_preprocessing (text):
    # Casefolding
    cleaned_text = text.lower()
    # Hapus noise
    cleaned_text = re.sub(r'@\w+|#\w+', '', cleaned_text)
    cleaned_text = cleaned_text.encode('ascii', 'ignore').decode('ascii')
    cleaned_text = re.sub(r'[0-9]+', '', cleaned_text)
    cleaned_text = re.sub(r'[^\w\s]', ' ', cleaned_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    raw_tokens = cleaned_text.split()

    filtered_tokens = [t for t in raw_tokens if t not in sw_sastrawi and len(t) >= 3]

    tokens =  [stemmer.stem(t) for t in filtered_tokens]

    return ' '.join(tokens), tokens

def build_inverted_index(df):
    inverted_index = {}

    for _, row in df.iterrows():
        doc_id = str(row['id_str'])
        text = row['full_text']

        _, tokens = text_preprocessing(text)
        if not tokens:
            continue

        for token in tokens:
            if token not in inverted_index:
                inverted_index[token] = {}
            inverted_index[token][doc_id] = inverted_index[token].get(doc_id, 0) + 1
    return inverted_index

def calculated_tfidf(inverted_index: dict, total_docs: int):
    tfidf_index = {}
    idf_dict = {}
    doc_length_sq = {}

    for term, doc_dict in inverted_index.items():
        df_t = len(doc_dict)
        idf = math.log10((total_docs + 1) / (df_t + 1)) + 1
        idf_dict[term] = idf
        
        tfidf_index[term] = {}
        for doc_id, raw_tf in doc_dict.items():
            log_tf = (1 + math.log10(raw_tf)) if raw_tf > 0 else 0
            weight = log_tf * idf
            tfidf_index[term][doc_id] = weight

            doc_length_sq[doc_id] = doc_length_sq.get(doc_id, 0) + weight ** 2

    doc_magnitudes = {
        doc_id: math.sqrt(sq)
        for doc_id, sq in doc_length_sq.items()
    }
    return tfidf_index, idf_dict, doc_magnitudes

def search(query: str, tfidf_index: dict, idf_dict: dict, doc_magnitudes: dict, doc_lookup: dict):
    _, query_tokens = text_preprocessing(query)
    if not query_tokens:
        return []
    
    query_raw_tf: dict = {}
    for token in query_tokens:
        query_raw_tf[token] = query_raw_tf.get(token, 0) + 1

    query_tfidf = {}
    query_length_sq = 0.0

    for term, raw_tf in query_raw_tf.items():
        if term not in idf_dict:
            continue
        log_tf = (1 + math.log10(raw_tf)) if raw_tf > 0 else 0
        weight = log_tf * idf_dict[term]
        query_tfidf[term] = weight
        query_length_sq += weight ** 2

    if query_length_sq == 0:
        return []
    
    query_magnitude = math.sqrt(query_length_sq)

    dot_products: dict = {}
    for term, q_weight in query_tfidf.items():
        if term in tfidf_index:
            for doc_id, d_weight in tfidf_index[term].items():
                dot_products[doc_id] = dot_products.get(doc_id, 0) + (q_weight * d_weight)

    if not dot_products:
        return []

    scores = []
    for doc_id, dot_prod in dot_products.items():
        denom = query_magnitude  * doc_magnitudes.get(doc_id, 1.0)
        if denom == 0:
            continue
        similarity = dot_prod / denom
        
        row_data = doc_lookup[doc_id]
        scores.append({
            "id_str": doc_id,
            "full_text": row_data['full_text'],
            "score": round(similarity, 4)
        })

    scores = sorted(scores, key=lambda x: x['score'], reverse=True)

    return scores

