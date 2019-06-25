

import os
import string
import pprint
import random

word_count = dict()

def strip_line(line):
    line = line.strip()
    line = line.replace('-', ' ')
    line = line.replace("”", '')
    line = line.replace("“", '')
    line = line.replace("’", "'")
    line = line.replace("‘", "'")
    line = line.replace("\xa0", "'")
    line = line.replace("\ufeff", "'")
    return line

def add_word_to_count(word, next_word):
    if (word != '') and (next_word != ''):
        if word in word_count:
            try:
                word_count[word].append(next_word)
            except:
                pass
        else:
            try:
                word_count[word] = [next_word]
            except:
                pass

def scrap_texts():
    text_dir = os.getcwd() + '\\markov_chain\\text_files'
    #print(os.listdir(text_dir))
    for text in os.listdir(text_dir):
        path = text_dir + '\\' + text
        with open(path, 'rb') as fin:
            for line in fin:
                try:
                    line = strip_line(line.decode())
                    line = line.split(' ')
                    last_word = line[len(line)-1]
                    for i, word in enumerate(line):
                        if i == 0:
                            add_word_to_count(last_word, word)
                            add_word_to_count(word, line[i + 1])
                        else:
                            add_word_to_count(word, line[i + 1])
                except:
                    pass

def print_word_count():
    for word in word_count:
        print(word, word_count[word])

def add_word(word):
    if word != '':
        if word in word_count:
            word_count[word] += 1
            #print(f'The word count for "{word}" went up by one.')
        else:
            word_count[word] = 1
            #print(f'I aded "{word}" to dictionary.')

def get_random_from_list(listed_items):
    return listed_items[random.randint(0, len(listed_items) - 1)]


def word_selection(word):
    listed_items = word_count.get(word, ['the', 'of', 'a', ])
    return listed_items[random.randint(0, len(listed_items) - 1)]

def random_sentence(seed):
        print(seed, end =' ')
        previous_word = seed
        while list(previous_word)[-1] not in ['!', '?', '.']:
            previous_word = word_selection(previous_word)
            if previous_word not in word_count:
                print(f'***ERROR:{previous_word}***', end = '')
                previous_word = word_selection(previous_word)
            print(previous_word, end = ' ')

scrap_texts() #we built the words that come after a word.

for i in range(1000):
    print(i)
    random_sentence('The')
