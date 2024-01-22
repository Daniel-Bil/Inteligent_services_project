import json
import os
import re

import numpy as np

from classificator import classify

pattern = r'\b\w+\b'

if __name__ == '__main__':
    files_path = f'./pages'
    files = os.listdir(files_path)
    all_words = []
    # for file_name in files:
    #     path = f"{files_path}/{file_name}"
    #     try:
    #         with open(path, "r") as file:
    #             d = json.load(file)
    #
    #
    #
    #         words = list(set([word.lower() for word in re.findall(pattern, d["Summary"])]))
    #         print(len(words), words)
    #         all_words = all_words + words
    #     except:
    #         print("ERROR", file_name)
            # os.remove(path)

    # with open("./dictionary","w") as f:
    #     json.dump(list(set(all_words)), f, indent=4)

    with open("./dictionary","r") as f:
        ff = json.load(f)
    print(len(ff))
    vectors = []
    for file_name in files:
        path = f"{files_path}/{file_name}"
        print(file_name)
        try:
            with open(path, "r") as file:
                d = json.load(file)

            words = [w.lower() for w in re.findall(pattern, d["Summary"])]
            bov = np.zeros(len(ff))
            for word in words:
                id = ff.index(word)
                bov[id]+=1
            vectors.append(bov)


        except:
            print("ERROR", file_name)
            raise Exception("jebac pis")
    for i in range(50):
        print(len(vectors[i]))
        print(sum(vectors[i]))
    vectors = np.array(vectors)
    np.save("./vectors.npz", vectors)
    preds = classify(vectors,0)
    print(preds[:10])








