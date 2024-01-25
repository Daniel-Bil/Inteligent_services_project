import json
import os
import re
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib.lines import Line2D
from sklearn.decomposition import PCA
import nltk
from nltk.corpus import stopwords

from classificator import classify, AlgorithmType

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

            stop_words = set(stopwords.words('english'))
            words = [w.lower() for w in re.findall(pattern, d[key_in_dictionary]) if w.lower() not in stop_words]
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

def plot_graph(files, number_of_categories):
    G = nx.Graph()

    # Prepare a list of distinct colors, one for each category
    distinct_colors = plt.cm.get_cmap('tab20', number_of_categories)

    # Add category nodes with distinct colors
    for i in range(number_of_categories):
        G.add_node(f"Cluster{i}", type='category', color=distinct_colors(i), size=300)

    # Add article nodes and connect them to their respective category
    for i, file_name in enumerate(files):
        category_index = preds[i]
        G.add_node(file_name, type='article', color=distinct_colors(category_index), size=50)
        G.add_edge(file_name, f"Cluster{category_index}", weight=1)

    # Generate a color map and size list
    color_map = [G.nodes[node]['color'] for node in G]
    size_list = [G.nodes[node]['size'] for node in G]

    # Generate positions for each node
    pos = nx.spring_layout(G, k=0.5, iterations=100)

    # Draw the nodes with the color map and size list
    nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=size_list)

    # Draw the edges with varying thickness
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    nx.draw_networkx_edges(G, pos, width=weights)

    # Draw labels for categories only
    category_labels = {node: node for node in G.nodes if G.nodes[node]['type'] == 'category'}
    nx.draw_networkx_labels(G, pos, labels=category_labels, font_size=10)

    # Set the plot size
    plt.figure(figsize=(12, 8))

    # Turn off the axis
    plt.axis('off')

    # Show the plot
    plt.show()


def show_dendogram(vectors, cluster_labels):
    Z = linkage(vectors, method='ward')

    labels = [f"Cluster {label}" for i, label in enumerate(cluster_labels)]

    plt.figure(figsize=(25, 10))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('Index or Cluster Size')
    plt.ylabel('Distance')

    dendrogram(
        Z,
        truncate_mode='lastp',
        labels=labels,
        leaf_rotation=90.,
        leaf_font_size=12.,
        show_contracted=True,
    )

    plt.show()


if __name__ == '__main__':
    nltk.download('stopwords')

    files_path = f'./pages'

    files = os.listdir(files_path)

    num_files_to_select = 300

    files = random.sample(files, min(num_files_to_select, len(files)))

    all_words = []

    vectors = create_vectors(files, "Summary", 1)
    vectors = np.array(vectors)

    # np.save("./vectors.npz", vectors)

    preds = classify(vectors, AlgorithmType.AgglomerativeClustering)
    show_dendogram(vectors, preds)

    preds = classify(vectors, AlgorithmType.KMeans)
    plot_graph(files, 10)


    print(preds[:100])


    res = group_articles_based_on_prediction(files, preds, 10)












