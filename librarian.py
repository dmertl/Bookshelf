"""
Librarian will create a viewable index of ebooks in any directory

Creates shelf.xml and extracts cover images to covers/
"""

import sys
from bookshelf.librarian import Librarian

if len(sys.argv) == 2:
    lib = Librarian()
    lib.process(sys.argv[1])
else:
    print 'Invalid syntax. {} directory'.format(sys.argv[0])