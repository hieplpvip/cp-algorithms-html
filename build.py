#!/usr/bin/env python3

from pathlib import Path
import re
import shutil
import subprocess

import dload

CP_ALGORITHMS_URL = 'https://github.com/cp-algorithms/cp-algorithms/archive/master.zip'
CP_ALGORITHMS_DIR = Path('cp-algorithms-master')
BUILD_DIR = Path('build')

if __name__ == '__main__':
    print('Downloading cp-algorithms...')
    shutil.rmtree(CP_ALGORITHMS_DIR, ignore_errors=True)
    dload.save_unzip(CP_ALGORITHMS_URL, '.', True)

    print('Modifying mkdocs.yml...')
    with open(CP_ALGORITHMS_DIR / 'mkdocs.yml', 'r', encoding='utf8') as f:
        config = f.read()
    config = config.replace('https://polyfill.io/v3/polyfill.min.js?features=es6', 'javascript/polyfill.min.js')
    config = config.replace('https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js', 'javascript/tex-mml-chtml.js')
    with open(CP_ALGORITHMS_DIR / 'mkdocs.yml', 'w', encoding='utf8') as f:
        f.write(config)

    print('Building...')
    subprocess.run('mkdocs build', shell=True, cwd=CP_ALGORITHMS_DIR, check=True)
    shutil.rmtree('build', ignore_errors=True)
    shutil.copytree(CP_ALGORITHMS_DIR / 'public', BUILD_DIR)

    print('Downloading assets...')
    JAVASCRIPT_DIR = BUILD_DIR / 'javascript'
    WOFF_DIR = JAVASCRIPT_DIR / 'output/chtml/fonts/woff-v2'
    WOFF_DIR.mkdir(parents=True, exist_ok=True)
    dload.save('https://polyfill.io/v3/polyfill.min.js?features=es6', str(JAVASCRIPT_DIR / 'polyfill.min.js'))
    dload.save('https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js', str(JAVASCRIPT_DIR / 'tex-mml-chtml.js'))
    with open(BUILD_DIR / 'javascript/tex-mml-chtml.js', 'r', encoding='utf8') as f:
        mathjax = f.read()
    for woff in re.finditer(r'%%URL%%\/(MathJax_[^ ]*\.woff)', mathjax):
        woff = woff.group(1)
        dload.save('https://unpkg.com/mathjax@3/es5/output/chtml/fonts/woff-v2/' + woff, str(WOFF_DIR / woff))
