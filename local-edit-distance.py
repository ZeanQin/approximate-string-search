#!/usr/bin/python -tt

import sys, string, os, re
import lib.alignment 

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

def main():
  titles_dictionary = build_titles_dictionary()
  try:
    revs_filenames = os.listdir('./revs/')
  except OSError:
    print 'Error: cannot find the ./revs/ directory. Please make sure it is placed in the same folder.'
    sys.exit(1)

  total_revs = len(revs_filenames)
  processed_revs = 0
  
  print 'Analysing the reviews using Smith-Waterman algorithm....'
  for filename in revs_filenames:
    result_tuples = []
    try:
      f = open('./revs/' + filename, 'r')
    except IOError:
      print 'File ', filename, ' is not found, Program will continue.' 
    text = f.read()
    for key in titles_dictionary.keys():
      cmp_result = lib.alignment.water(key, text)
      # reject titles with a matching score less than 1
      if cmp_result >= 1:
        result_tuples.append((key, cmp_result))
    sorted_tuples = sorted(result_tuples, key=get_score, reverse=True)
    
    # save the output to a file 
    if not os.path.exists('./result/'):
      os.mkdir('./result/')
    if not os.path.exists('./result/local-edit-distance/'):
      os.mkdir('./result/local-edit-distance/')
    fw = open('./result/local-edit-distance/' + filename, 'w')
    fw.write('\n'.join('%s %s' % x for x in sorted_tuples))

    f.close()
    fw.close()
    processed_revs += 1
    print 'Progress: %d out of %d reviews are completed' % (processed_revs, total_revs)

if __name__ == '__main__':
  main()
