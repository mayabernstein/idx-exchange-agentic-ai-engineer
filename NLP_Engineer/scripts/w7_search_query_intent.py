from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class QueryIntentClassifier: 
    def __init__(self): 
        self.vectorizer = TfidfVectorizer(max_features=500) 
        self.model = LogisticRegression(max_iter=1000) 
        self.labels = [ 
            'browsing', 
            'researching', 
            'high_intent_inquiry' 
        ] 

    def train(self, queries, labels): 
        X = self.vectorizer.fit_transform(queries) 
        self.model.fit(X, labels) 

    def predict(self, query): 
        X = self.vectorizer.transform([query]) 
        probas = self.model.predict_proba(X)[0] 
        intent = self.model.classes_[probas.argmax()] 
        confidence = probas.max() 

        return intent, confidence