from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.exceptions import NotFittedError

class RecipeModel:
    def __init__(self):
        self.model = make_pipeline(TfidfVectorizer(), MultinomialNB())
        self.is_trained = False

    def train(self, X, y):
        self.model.fit(X, y)
        self.is_trained = True

    def generate_recipe(self, dish_name):
        if not self.is_trained:
            return None
        try:
            prediction = self.model.predict([dish_name])[0]
            if prediction in self.model.steps[-1][1].classes_:
                return prediction
            else:
                return None
        except NotFittedError:
            return None