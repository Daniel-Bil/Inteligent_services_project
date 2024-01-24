from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.naive_bayes import GaussianNB
import numpy as np



def classify(data, alg=0):
    print("classify")
    if alg == 0:
        classifier = KMeans(n_clusters=10)
    elif alg == 1:
        classifier = AgglomerativeClustering()
    elif alg == 2:
        classifier = GaussianNB()
    else:
        raise Exception("NO CHOSEN ALGORITHM")
    pred = classifier.fit_predict(data)
    return pred





