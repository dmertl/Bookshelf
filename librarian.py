"""
Librarian will create a viewable index of ebooks in any directory

Creates shelf.xml and extracts cover images to covers/
"""
# TODO: unit tests
# TODO: test on more ebooks
# TODO: better coverage on alternate specifications for cover image
# TODO: styling of shelf.xml XSLT is necessary for images
# TODO: some kind of alert or visibility into files with missing data
# TODO: interactive elements with JS?
# TODO: search for cover images that have no matching ebook and remove them
# TODO: save time by not processing ebooks that have not been modified. store modified date or checksum

import sys
from bookshelf import Shelf

if len(sys.argv) == 2:
    shelf = Shelf(sys.argv[1])
else:
    print 'Invalid syntax. {} directory'.format(sys.argv[0])