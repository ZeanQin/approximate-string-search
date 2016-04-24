#!/usr/bin/env python

import sys, string, os, re

# read the film titles in 'film_titles.txt' into a dictionary and returns the result dictionary
def build_titles_dictionary():
  titles_dictionary = {}
  try:
    f = open('film_titles.txt', 'r')
  except IOError: 
    print 'File "film_titles.txt" is not found, please make sure it is placed in the same directory as this file.'
    sys.exit(1)
  for line in f:
    titles_dictionary[string.strip(line)] = 1
  return titles_dictionary

def get_score(t):
  return t[1]

def levenshtein(a,b):
  "Calculates the Levenshtein distance between a and b."
  n, m = len(a), len(b)
  if n > m:
    # Make sure n <= m, to use O(min(n,m)) space
    a,b = b,a
    n,m = m,n

  current = range(n+1)
  for i in range(1,m+1):
    previous, current = current, [i]+[0]*n
    for j in range(1,n+1):
      add, delete = previous[j]+1, current[j-1]+1
      change = previous[j-1]
      if a[j-1] != b[i-1]:
        change = change + 1
      current[j] = min(add, delete, change)
  return current[n]

def main():
  titles_dictionary = build_titles_dictionary()
  try:
    revs_filenames = os.listdir('./revs/')
  except OSError:
    print 'Error: cannot find the ./revs/ directory. Please make sure it is placed in the same folder.'
    sys.exit(1)

  total_revs = len(revs_filenames)
  processed_revs = 0
  
  print 'Analysing the reviews using Levenshtein algorithm....'
  for filename in revs_filenames:
    result_tuples = []
    try:
      f = open('./revs/' + filename, 'r')
    except IOError:
      print 'File ', filename, ' is not found, Program will continue.' 
    text = f.read()
    for key in titles_dictionary.keys():
      # explode each key and the review text into a list of words. Use leveshtein algorithm to calculate the distance, take the shorted distance for each word, add the lowest cost for each word in the key together and calculate the average. 
      word_score_dict = {}
      key_words = key.split()
      file_words = text.split()
      for key_word in key_words:
        for file_word in file_words:
          score = levenshtein(key_word, file_word)
          if (not key_word in word_score_dict.keys()) or word_score_dict.get(key_word) > score:
            word_score_dict[key_word] = score
      key_score = 0
      for value in word_score_dict.values():
        key_score += value
      key_score = key_score/float(len(word_score_dict))
      result_tuples.append((key, key_score))
    sorted_tuples = sorted(result_tuples, key=get_score) 
     
    # save the output to a file 
    if not os.path.exists('./result/'):
      os.mkdir('./result/')
    if not os.path.exists('./result/levenshtein/'):
      os.mkdir('./result/levenshtein/')
    fw = open('./result/levenshtein/' + filename, 'w')
    fw.write('\n'.join('%s %s' % x for x in sorted_tuples))

    f.close()
    fw.close()
    processed_revs += 1
    print 'Progress: %d out of %d reviews are completed' % (processed_revs, total_revs)

if __name__ == '__main__':
  main()
    
