# -*- coding: utf-8 -*-
# Author : zenk
# 2016-03-02 12:49

'''
从喜马拉雅电台下载专辑

替换地址 _album_urls
'''
import itertools
import os.path
import re
import requests

_album_urls = [
  'http://www.ximalaya.com/7545862/album/292700'
]

def _extra_sounds(album_url_):
  text = requests.get(album_url_).text
  pattern = r'<li sound_id="(\d+)">'
  return map(lambda o : (o["title"], o["play_path_64"]),
             (requests.get("http://www.ximalaya.com/tracks/" + id + ".json").json()
              for id in set([m.group(1) for m in re.finditer(pattern, text)])))


def _download(sounds):
  '''
  @param sounds {"name": "name", "url": "url"}
  '''
  def _filename(name, url):
    return name + url[url.rfind('.'):]

  def print_url(r, *args, **kwargs):
    print(r.url)
	
  for name, url in filter(lambda s: not os.path.exists(_filename(*s)), sounds):
    with open(name + url[url.rfind('.'):], mode='bw') as o:
      print('download ' + url + ', save as ' + o.name)
      try:
        resp = requests.get(url, timeout=20, hooks=dict(response=print_url))
      except Exception as e:
        print(e)
      else:
        print('file size %s' % resp.headers['Content-Length'])
        o.write(requests.get(url).content)
      print('download ' + o.name + ' finished')

def main():
  _download(itertools.chain(*[_extra_sounds(url) for url in _album_urls]))

if __name__ == "__main__":
  main()
