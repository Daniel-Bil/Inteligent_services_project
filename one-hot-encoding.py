from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

encoder = LabelEncoder()
dictionary_labels = encoder.fit_transform(dictionary.py)
dictionary_labels


encoder = OneHotEncoder(sparse=False)
city_labels = dictionary_labels.reshape((5, 1))
encoder.fit_transform(city_labels)