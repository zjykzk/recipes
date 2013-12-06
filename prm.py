# -*- coding: utf-8 -*-
# Author : zenk
# 2013-12-02 16:12
import fnmatch
import optparse
import os
'''
remove the files whose names are matched by UNIX shell-stype 
wildcard characters

example:
  remove the .test files
  python rm_files.py -d dir -p *.test
'''

_OPT = optparse.OptionParser()
_OPT.add_option("-d", action = "store", dest = "search_dir",
    help = "the search directory")
_OPT.add_option("-p", action = "store", dest = "pattern",
    help = "the search pattern")

def _is_match(patterns, path):
  for pattern in patterns:
    if fnmatch.fnmatch(path, pattern):
      return True
  return False

def main(search_dir, pattern):
  opts, _ = _OPT.parse_args()
  search_dir, pattern = opts.search_dir, opts.pattern
  if not search_dir or not pattern:
    print "please input the search directory and file pattern"
    exit(-1)

  patterns = pattern.split(',')
  print ','.join(patterns)
  for path, dirs, files in os.walk(search_dir):
    for file in files:
      full_path = os.path.join(path, file)
      if _is_match(patterns, full_path):
        print "removing %s" % full_path
        os.remove(full_path)

if __name__ == "__main__":
  main(search_dir, pattern)
