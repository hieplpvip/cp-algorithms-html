#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import shutil
import dload
import datetime
import markdown
import fnmatch
from distutils.dir_util import copy_tree

E_MAXX_ENG_URL = 'https://github.com/e-maxx-eng/e-maxx-eng/archive/master.zip'
E_MAXX_ENG_DIR = 'e-maxx-eng-master/src/'
param_pattern = r'^\s*\<\!\-\-\?([a-z]+)\s+(.*)\-\-\>\s*$'

with open('src/templates/default.html') as f:
  htmlTemplate = f.read()


def init():
  shutil.rmtree(E_MAXX_ENG_DIR)
  dload.save_unzip(E_MAXX_ENG_URL, '.', True)

  shutil.rmtree('build', ignore_errors=True)
  os.mkdir('build')
  copy_tree('src/static', 'build')


def listMarkdownFiles():
  markdownFiles = []
  for root, dirnames, filenames in os.walk(E_MAXX_ENG_DIR):
    for filename in fnmatch.filter(filenames, '*.md'):
      markdownFiles.append(os.path.join(root, filename)[len(E_MAXX_ENG_DIR):])

  return markdownFiles


def substituteParams(text, params):
  for key, value in params.items():
    text = text.replace('&' + key + '&', value)
  return text


def convertFile(file):
  with open(E_MAXX_ENG_DIR + file, 'r') as f:
    lines = f.readlines()
  new_lines = []
  params = {}
  for line in lines:
    param = re.search(param_pattern, line)
    if param:
      params[param.group(1)] = param.group(2)
    else:
      new_lines.append(line)

  if 'template' in params and params['template'] != 'default':
    return

  text = '\n'.join(new_lines)
  params['text'] = markdown.markdown(text, extensions=['extra'])
  params['baseurl'] = '../' * file.count('/')
  params['year'] = str(datetime.datetime.now().year)

  html = substituteParams(htmlTemplate, params)

  file = 'build/' + file.replace('.md', '.html')
  os.makedirs(os.path.dirname(file), exist_ok=True)
  with open(file, 'w') as f:
    f.write(html)


if __name__ == '__main__':
  init()
  markdownFiles = listMarkdownFiles()
  for file in markdownFiles:
    convertFile(file)
