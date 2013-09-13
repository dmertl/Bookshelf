"""
Librarian will create a viewable index of ebooks in any directory

Creates shelf.xml and extracts cover images to covers/
"""

import sys
from bookshelf.Shelf import Shelf

if len(sys.argv) == 2:
    shelf = Shelf(sys.argv[1])
else:
    print 'Invalid syntax. {} directory'.format(sys.argv[0])