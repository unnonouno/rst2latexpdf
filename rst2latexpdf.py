#!/usr/bin/env python

platex = 'platex'
dvipdfmx = 'dvipdfmx'

import sys
import os
from subprocess import Popen

def print_usage():
    print 'rst2latexpdf.py rstfile'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    input_file = sys.argv[1]
    base = input_file[0: input_file.rfind('.')]
    
    with open(input_file) as f:
        text = f.read()
    from docutils.writers.latex2e import Writer
    from docutils.core import publish_parts
    settings = {
        'documentoptions': 'a4j',
        'documentclass': 'jarticle',
        }
    w = Writer()
    r = publish_parts(text, writer=w, settings_overrides=settings)
    import tempfile
    dir = tempfile.mkdtemp()

    #global config
    #platex = config['platex']
    #dvipdfmx = config['dvipdfmx']

    try:
        with open(os.path.join(dir, 'temp.tex'), 'w') as f:
            f.write(r['whole'].encode('utf-8'))
        Popen([platex, '-jobname=temp', '-output-directory=%s' % dir,
               '-interaction=nonstopmode',
               os.path.join(dir, 'temp.tex')]).wait()
        Popen([dvipdfmx,
               '-o', base + '.pdf',
               os.path.join(dir, 'temp.dvi')]).wait()
    finally:
        import shutil
        shutil.rmtree(dir)
