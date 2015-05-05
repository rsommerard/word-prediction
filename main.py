# coding=utf-8

import string
import pickle
import os


def extract_unigrams(words):
    unigrams_tab = []
    word1 = ''
    word2 = ''
    i = -1
    for word in words:
        if i == -1:
            word1 = word
            i = 1
        elif(i == 0):
            word1 = word
            unigrams_tab.append((word2, word1))
            i = 1
        else:
            word2 = word
            unigrams_tab.append((word1, word2))
            i = 0

    return unigrams_tab


def extract_bigrams(words):
    unigrams = extract_unigrams(words)
    bigrams_tab = []
    unigram1 = ('', '')
    unigram2 = ('', '')
    i = -1
    for unigram in unigrams:
        if i == -1:
            unigram1 = unigram
            i = 1
        elif(i == 0):
            unigram1 = unigram
            bigrams_tab.append((unigram2, unigram1))
            i = 1
        else:
            unigram2 = unigram
            bigrams_tab.append((unigram1, unigram2))
            i = 0

    return bigrams_tab


def unigrams_process():
    unigrams = {}

    with open('sentences.txt', 'r', encoding='utf8') as file:
        line = file.readline()
        i = 1
        while(line):
            if i % 1000 == 0:
                print('Unigrams: ' + str(i))
            line = line.lower()
            line = ''.join(char for char in line if char not in set(string.punctuation))
            words = line.split()
            words.pop(0)

            for unigram1, unigram2 in extract_unigrams(words):
                if unigram1 in unigrams:
                    if unigram2 in unigrams[unigram1]:
                        continue

                    unigrams[unigram1].append(unigram2)
                else:
                    unigrams[unigram1] = [unigram2]

            line = file.readline()
            i += 1

    unigrams_serializer(unigrams)

    return unigrams


def wunigrams_process():
    wunigrams = {}

    with open('sentences.txt', 'r', encoding='utf8') as file:
        line = file.readline()
        i = 1
        while(line):
            line = line.lower()
            if i % 1000 == 0:
                print('Wunigrams: ' + str(i))
            line = ''.join(char for char in line if char not in set(string.punctuation))
            words = line.split()
            words.pop(0)

            for entry in extract_unigrams(words):
                if entry in wunigrams:
                    wunigrams[entry] += 1
                else:
                    wunigrams[entry] = 1

            line = file.readline()
            i += 1

    wunigrams_serializer(wunigrams)

    return wunigrams


def wbigrams_process():
    wbigrams = {}

    with open('sentences.txt', 'r', encoding='utf8') as file:
        line = file.readline()
        i = 1
        while(line):
            line = line.lower()
            if i % 1000 == 0:
                print('Wbigrams: ' + str(i))
            line = ''.join(char for char in line if char not in set(string.punctuation))
            words = line.split()
            words.pop(0)

            for entry in extract_bigrams(words):
                if entry in wbigrams:
                    wbigrams[entry] += 1
                else:
                    wbigrams[entry] = 1

            line = file.readline()
            i += 1

    wbigrams_serializer(wbigrams)

    return wbigrams


def bigrams_process():
    bigrams = {}

    with open('sentences.txt', 'r', encoding='utf8') as file:
        line = file.readline()
        i = 1
        while(line):
            if i % 1000 == 0:
                print('Bigrams: ' + str(i))
            line = line.lower()
            line = ''.join(char for char in line if char not in set(string.punctuation))
            words = line.split()
            words.pop(0)

            for bigram1, bigram2 in extract_bigrams(words):
                if bigram1 in bigrams:
                    if bigram2 in bigrams[bigram1]:
                        continue

                    bigrams[bigram1].append(bigram2)
                else:
                    bigrams[bigram1] = [bigram2]

            line = file.readline()
            i += 1

    bigrams_serializer(bigrams)

    return bigrams


def wunigrams_serializer(dict):
    with open('wunigrams', 'wb') as file:
        pickle.dump(dict, file)


def unigrams_serializer(dict):
    with open('unigrams', 'wb') as file:
        pickle.dump(dict, file)


def wunigrams_deserializer():
    with open('wunigrams', 'rb') as file:
        return pickle.load(file)


def unigrams_deserializer():
    with open('unigrams', 'rb') as file:
        return pickle.load(file)


def wbigrams_serializer(dict):
    with open('wbigrams', 'wb') as file:
        pickle.dump(dict, file)


def bigrams_serializer(dict):
    with open('bigrams', 'wb') as file:
        pickle.dump(dict, file)


def bigrams_deserializer():
    with open('bigrams', 'rb') as file:
        return pickle.load(file)


def wbigrams_deserializer():
    with open('wbigrams', 'rb') as file:
        return pickle.load(file)


if __name__ == '__main__':
    wunigrams = {}
    unigrams = {}
    wbigrams = {}
    bigrams = {}

    if os.path.exists('wunigrams'):
        wunigrams = wunigrams_deserializer()
    else:
        wunigrams = wunigrams_process()

    if os.path.exists('wbigrams'):
        wbigrams = wbigrams_deserializer()
    else:
        wbigrams = wbigrams_process()

    if os.path.exists('unigrams'):
        unigrams = unigrams_deserializer()
    else:
        unigrams = unigrams_process()

    if os.path.exists('bigrams'):
        bigrams = bigrams_deserializer()
    else:
        bigrams = bigrams_process()

    sentence = input("Phrase: ")

    while(sentence != 'q'):
        sentence = ''.join(char for char in sentence if char not in set(string.punctuation))
        words = sentence.split()

        if len(words) > 1:
            if (words[-2].lower(), words[-1].lower()) in bigrams:
                prediction_words = bigrams[(words[-2].lower(), words[-1].lower())]
            else:
                prediction_words = []

            propositions = []
            for i in range(3):
                best = None
                for word in prediction_words:
                    if best == None:
                        best = word
                        continue

                    if wbigrams[((words[-2].lower(), words[-1].lower()), word)] > wbigrams[((words[-2].lower(), words[-1].lower()), best)]:
                        best = word

                if best != None:
                    prediction_words.remove(best)
                    propositions.append(best)

            while(len(propositions) < 3):
                propositions.append(('', ''))

            _, mot1 = propositions[0]
            _, mot2 = propositions[1]
            _, mot3 = propositions[2]
        else:
            if words[-1].lower() in unigrams:
                prediction_words = unigrams[words[-1].lower()]
            else:
                prediction_words = []

            propositions = []
            for i in range(3):
                best = ''
                for word in prediction_words:
                    if best == '':
                        best = word
                        continue

                    if wunigrams[(words[-1].lower(), word)] > wunigrams[(words[-1].lower(), best)]:
                        best = word

                if best != '':
                    prediction_words.remove(best)

                propositions.append(best)

            while(len(propositions) < 3):
                propositions.append('')

            mot1 = propositions[0]
            mot2 = propositions[1]
            mot3 = propositions[2]

        if mot3 == '':
            if mot2 == '':
                if mot1 == '':
                    print('Pas de propositions.')
                else:
                    print('Propositions: ' + mot1)
            else:
                print('Propositions: ' + mot1 + ' | ' + mot2)
        else:
            print('Propositions: ' + mot1 + ' | ' + mot2 + ' | ' + mot3)

        sentence = input("Phrase: ")
