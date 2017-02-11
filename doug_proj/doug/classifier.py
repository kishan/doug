from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np

def article_body(url):
    payload = {'token': '7bee659e1dfff58612ec9d453ff4cc24', 'url': url}
    req_url = 'https://api.diffbot.com/v3/article'
    res = requests.get(req_url, params=payload).json()
    words = res['objects'][0]['text'].splitlines()
    content = ' '.join(words)
    return content

def classify(article_url):
    keywords = [] #bag of words
    categories = []
    for line in open('data.txt'):
        line=line.strip()
        if len(line) > 0:
            category, *tokens = line.split()
            features = [t for t in tokens] #extracts each word from column
            keywords.append(' '.join(features)) #combines word to sentence
            categories.append(category)
    keywords = np.array(keywords)
    categories = np.array(categories)
    vectorizer = CountVectorizer()
    feature_vectors = vectorizer.fit_transform(keywords)
    tfidf_transformer = TfidfTransformer(use_idf=False).fit(feature_vectors)
    X_train_tfidf = tfidf_transformer.fit_transform(feature_vectors)
    clf = MultinomialNB().fit(X_train_tfidf, categories)
    docs_new = [article_body(article_url)]
    X_new_counts = vectorizer.transform(docs_new)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)
    predicted = clf.predict(X_new_tfidf)
    return(predicted[0])
