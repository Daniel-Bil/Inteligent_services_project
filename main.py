import json
import os
import re

import numpy as np

from classificator import classify

pattern = r'\b\w+\b'


class VectorType:
    OneHotEncoding = 0
    Histogram = 1

def create_vectors(files, key_in_dictionary, operation_type=1):

    vectors = []

    with open("./dictionary","r") as f:
        ff = json.load(f)

    for file_name in files:
        path = f"{files_path}/{file_name}"
        try:
            with open(path, "r") as file:
                d = json.load(file)

            words = [w.lower() for w in re.findall(pattern, d[key_in_dictionary])]
            bov = np.zeros(len(ff))
            for word in words:
                id = ff.index(word)
                bov[id] += 1

            if operation_type == VectorType.OneHotEncoding:
               for i in range(len(bov)):
                   if bov[i] > 1:
                       bov[i] = 1

            vectors.append(bov)

        except:
            print("ERROR", file_name)

    return vectors


def group_articles_based_on_prediction(files, prediction, number_of_categories):
    directory_name = f'./pages'
    articles_grouped = [[] for i in range(number_of_categories)]

    files_path_to_index = []

    for i, file_name in enumerate(files):
        path = f"{directory_name}/{file_name}"
        files_path_to_index.append(path)

    for i in range(len(prediction)):
        index_of_group = prediction[i]

        with open(files_path_to_index[i], "r") as file:
            d = json.load(file)

        articles_grouped[index_of_group].append(d)

    return articles_grouped


if __name__ == '__main__':
    files_path = f'./pages'
    files = os.listdir(files_path)
    all_words = []

    vectors = create_vectors(files, "Summary", 1)
    vectors = np.array(vectors)

    # np.save("./vectors.npz", vectors)
    preds = classify(vectors, 0)

    print(preds[:10])

    res = group_articles_based_on_prediction(files, preds, 10)









