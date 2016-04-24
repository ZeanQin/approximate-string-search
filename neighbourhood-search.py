#!/usr/bin/python -tt

import sys, string, os, re, commands

def get_score(t):
  return t[1]

# read the 'film_titles.txt' in to a dictionary
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

def main():
  titles_dictionary = build_titles_dictionary()
  try:
    revs_filenames = os.listdir('./revs/')
  except OSError:
    print 'Error: cannot find the ./revs/ directory. Please make sure it is placed in the same folder.'
    sys.exit(1)

  total_revs = len(revs_filenames)
  processed_revs = 0
  
  print 'Analysing the reviews using AGREP ...'
  for filename in revs_filenames:
    result_tuples = []
    for key in titles_dictionary:
      key = re.sub("'", '', key)
      cmd = "agrep -s -9 '" + key + "' ./revs/" + filename
      (status, output) = commands.getstatusoutput(cmd)
      if not status: 
        result_tuples.append((key, output[0]))
    sorted_tuples = sorted(result_tuples, key=get_score)

    if not os.path.exists('./result/'):
      os.mkdir('./result/')
    if not os.path.exists('./result/neighbourhood-search/'):
      os.mkdir('./result/neighbourhood-search/')

    fw = open('./result/neighbourhood-search/' + filename, 'w')
    fw.write('\n'.join('%s %s' % x for x in sorted_tuples))
    fw.close()
    processed_revs += 1
    print 'Progress: %d out of %d reviews are completed' % (processed_revs, total_revs)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
