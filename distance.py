import math
import operator
import sqlite3
connection = sqlite3.connect('/Users/halleypark/PycharmProjects/Word Counter.db')
cursor = connection.cursor()


def get_titles():
    titles = []
    rows = cursor.execute('SELECT DISTINCT Title '
                          'FROM BOOKS')
    for title in rows:
        titles.append(title[0])
    return titles


def get_words(title):
    rows = cursor.execute('SELECT Word, Count '
                          'FROM Books '
                          'WHERE Title = ?', (title,)).fetchall()
    word_count = {}
    for words in rows:
        if words[0] not in word_count:
            word_count[words[0]] = words[1]
    return word_count


def distance(book_1, book_2):
    partial_sum = 0
    for word in book_1.keys() | book_2.keys():
        count_1 = 0
        count_2 = 0
        if word in book_1:
            count_1 = book_1[word]
        if word in book_2:
            count_2 = book_2[word]
        partial_sum += (count_1 - count_2) ** 2
    euclidean = math.sqrt(partial_sum)
    return euclidean


def get_distances(titles):
    distances = {}

    for t in range(len(titles)):
        for i in range(t+1, len(titles)):
            word_count_1 = get_words(titles[t])
            word_count_2 = get_words(titles[i])
            distances[(titles[t], titles[i])] = distance(word_count_1, word_count_2)

    return distances


def cluster(titles, distances):
    cluster_list = []
    for title in titles:
        cluster_list.append([title])
    sorted_distances = sorted(distances.items(), key=operator.itemgetter(1))
    index_counter = 0
    while len(cluster_list) > 3:
        print(cluster_list)

        # find next two clusters to combine
        book_1 = sorted_distances[index_counter][0][0]
        book_2 = sorted_distances[index_counter][0][1]
        for cluster in cluster_list:
            if book_1 in cluster:
                cluster_1 = cluster
            if book_2 in cluster:
                cluster_2 = cluster
        if cluster_1 != cluster_2:
            # combine those clusters
            cluster_1.extend(cluster_2)
            cluster_list.remove(cluster_2)
        index_counter += 1
    return cluster_list


titles = get_titles()
distances = get_distances(titles)
cluster_list = cluster(titles, distances)
print(cluster_list)
