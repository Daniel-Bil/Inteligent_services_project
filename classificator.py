from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.naive_bayes import GaussianNB
import numpy as np
from enum import Enum
class AlgorithmType(Enum):
    KMeans = 0,
    AgglomerativeClustering = 1,
    GaussianN = 2

def classify(data, alg=0):
    print("classify")
    if alg == AlgorithmType.KMeans:
        classifier = KMeans(n_clusters=10)
    elif alg == AlgorithmType.AgglomerativeClustering:
        classifier = AgglomerativeClustering(n_clusters=10, affinity='euclidean', linkage='ward')
        classifier.fit(data)
        return classifier.labels_
    elif alg == AlgorithmType.GaussianN:
        classifier = GaussianNB()
    else:
        raise Exception("NO CHOSEN ALGORITHM")
    pred = classifier.fit_predict(data)
    return pred





