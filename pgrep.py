# -*- coding: utf-8 -*-
# Author : zenk
# 2013-11-18 16:16
import collections
import optparse
import os
import re
import sys

import rarfile


'''
options configure
'''
_OPT = optparse.OptionParser()
_OPT.add_option("-p", action = "store", dest = "pattern", 
    help = "the searching pattern")
_OPT.add_option("-f", action = "store", dest = "filepath",
    help = "searching filepath")
_OPT.add_option("-a", action = "store", dest = "above",
    help = "lines count above satisfied line")
_OPT.add_option("-b", action = "store", dest = "below",
    help = "lines count below satisfied line")
_OPT.add_option("-e", action = "store_true", dest = "regex",
    help = "using regex")
_OPT.add_option("-n", action = "store_true", dest = "linenu",
    help = "show the line number")

class GrepInfo(object):
  def __init__(self, opts):
    self._pattern = opts.pattern
    self._filepath = opts.filepath
    self._above_count = int(opts.above) if opts.above else 0
    self._below_count = int(opts.below) if opts.below else 0
    self._linenu = opts.linenu
    self._regex = opts.regex
    self._nr = 0
    self._above_lines = collections.deque(maxlen = self._above_count) if self._above_count else None
    self._below_count_tracer = self._below_count if self._below_count else None
    self._last_match_line = -1

  def _open(self, filename):
    if rarfile.is_rarfile(filename):
      rf = rarfile.RarFile(filename)
      for f in rf.infolist():
        return rf.open(f.filename)
    return open(filename, 'r')

  def _filter(self, line):
    #return line[:line.find(',')] + line[line.find('=')+1:]
    return line

  def _doprint(self, line):
    '''
    print the line 
    '''
    print line,

  def _matching(self, line):
    self._flush_above()
    self._flush_below()
    self._print(line)
    self._last_match_line = self._nr

  def _is_matched(self, line):
    if self._regex:
      return re.search(self._pattern, line)

    return self._pattern in line

  def _print(self, line):
    '''
    first do the filter the unnecessory information, then print it
    print the line : line number : line
    '''
    ret = self._filter(line)
    self._doprint(ret if not self._linenu else "%d:%s" % (self._nr, ret))

  def _record_above(self, line):
    if self._above_lines is None:
      return

    self._above_lines.append((self._nr, line))

  def _flush_above(self):
    '''
    print the above lines and clear it
    '''
    if self._above_lines is None:
      return

    for line in self._above_lines:
      if line[0] < self._below_count + self._last_match_line:
        continue
      self._doprint("%d:%s" % (line[0], line[1]) if self._linenu else line[1])
    self._above_lines.clear()

  def _flush_below(self):
    if self._below_count_tracer is None:
      return

    self._below_count_tracer = self._below_count

  def _print_below(self, line):
    if not self._below_count_tracer:
      return

    if self._last_match_line < 0:
      return

    if self._below_count_tracer <= 0:
      return

    self._below_count_tracer -= 1
    self._doprint("%d:%s" % (self._nr, line) if self._linenu else line)
    
  def _grep(self):
    file = self._open(self._filepath)
    line = file.readline()
    while line:
      self._nr += 1

      if self._is_matched(line):
        self._matching(line)
      else:
        self._record_above(line)
        self._print_below(line)

      line = file.readline()
    file.close()

def _parse_opts():
  opts, _ = _OPT.parse_args()
  return GrepInfo(opts)

def main():
  grep = _parse_opts()
  if not grep._filepath or not grep._pattern:
    print opts
    exit(0)
  grep._grep()

if __name__ == '__main__':
  main()
