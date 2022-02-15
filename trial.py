from tkinter import X
import nltk

nltk.download("wordnet")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
from nltk.stem import WordNetLemmatizer

lematizer = WordNetLemmatizer()
x = "Vegetables are type of plants"
x_tokens = nltk.word_tokenize(x.lower())
pos_tags = nltk.pos_tag(x_tokens)
print(x_tokens)
