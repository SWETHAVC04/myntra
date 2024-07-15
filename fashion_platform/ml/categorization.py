from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

class AestheticCategorizer:
    def __init__(self):
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english')),
            ('clf', MultinomialNB()),
        ])

    def train(self, items, labels):
        """
        Train the categorizer on a set of items and their corresponding aesthetic labels.
        
        :param items: List of item descriptions
        :param labels: List of corresponding aesthetic labels
        """
        self.pipeline.fit(items, labels)

    def predict(self, items):
        """
        Predict the aesthetic category for a list of items.
        
        :param items: List of item descriptions
        :return: List of predicted aesthetic labels
        """
        return self.pipeline.predict(items)

    def predict_proba(self, items):
        """
        Predict the probability of each aesthetic category for a list of items.
        
        :param items: List of item descriptions
        :return: List of probability distributions over aesthetic labels
        """
        return self.pipeline.predict_proba(items)

# Example usage:
# categorizer = AestheticCategorizer()
# categorizer.train(['vintage floral dress', 'edgy leather jacket'], ['vintage', 'punk'])
# predictions = categorizer.predict(['colorful tie-dye shirt'])