import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import math

class FeatureExtractor:
    def __init__(self, url=""):
        self.url = url
        self.domain = url.split('//')[-1].split('/')[0]
    
    def url_entropy(self):
        url_trimmed = self.url.strip()
        entropy_distribution = [float(url_trimmed.count(c)) / len(url_trimmed) for c in dict.fromkeys(list(url_trimmed))]
        return -sum([e * math.log(e, 2) for e in entropy_distribution if e > 0])

    def digits_num(self):
        return len([i for i in self.url if i.isdigit()])

    def length(self):
        return len(self.url)

    def params_num(self):
        return len(self.url.split('&')) - 1

    def fragments_num(self):
        return len(self.url.split('#')) - 1

    def subdomain_num(self):
        return len(self.domain.split('.')) - 1

    def dom_ext(self):
        return self.domain.split('.')[-1]

    def has_http(self):
        return 'http' in self.url

    def has_https(self):
        return 'https' in self.url

    def is_ip(self):
        parts = self.domain.split('.')
        if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
            return True
        return False

    def run(self):
        return {
            "url": self.url,
            "entropy": self.url_entropy(),
            "digits": self.digits_num(),
            "url_length": self.length(),
            "param_nums": self.params_num(),
            "fragment_nums": self.fragments_num(),
            "subdomain_nums": self.subdomain_num(),
            "domain_extension": self.dom_ext(),
            "has_http": self.has_http(),
            "has_https": self.has_https(),
            "is_ip": self.is_ip(),
            "num_%20" : self.url.count("%20"),
            "num_@" : self.url.count("@")
        }




# Charger le modèle enregistré
model = load_model("MaliciousUrlDetector.h5")

# Charger le tokenizer
with open("tokenizer.pkl", "rb") as handle:
    tokenizer = pickle.load(handle)

# Charger l'encodeur de labels
with open("label_encoder.pkl", "rb") as handle:
    label_encoder = pickle.load(handle)

#url a tester
#new_url = "http://target-site.com*')(password=*))"
new_url = "https://youtube.com/watch?v=qnQ1vozGuEQ"

# extraction des caracteristiques
extractor = FeatureExtractor(new_url)
url_features = extractor.run()

#tokenisation
sequence = tokenizer.texts_to_sequences([new_url])
padded_sequence = pad_sequences(sequence, maxlen=100, padding='post', truncating='post')

extra_features = np.array([[url_features['entropy'], url_features['digits'],
                            url_features['url_length'], url_features['param_nums'],
                            url_features['has_http'], url_features['has_https'],
                            url_features['is_ip'], url_features['num_%20'],
                            url_features['num_@']]]).astype(np.int32)

# Faire la prediction
prediction = model.predict([padded_sequence, extra_features])
predicted_class = np.argmax(prediction, axis=1)
class_labels = label_encoder.inverse_transform(predicted_class)

print(f"Label predicted: {class_labels}")
print(f"Predictions: {prediction}")
