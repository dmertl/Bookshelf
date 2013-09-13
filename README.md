Bookshelf is a web based view of your ebook collection.

# TODO #

- get new OO organization working
- organize into proper module (file is module, so import bookshelf.shelf.Book would be import the Book class in file bookshelf/shelf.py)
- better coverage on alternate specifications for cover image
- styling of shelf.xml XSLT is necessary for images
- unit tests
- test on more ebooks
- some kind of alert or visibility into files with missing data
- interactive elements with JS?
- search for cover images that have no matching ebook and remove them
- save time by not processing ebooks that have not been modified. store modified date or checksum

# Key Features #

- Browsable with only filesystem access (no web server or scripting language)
- iTunes like display with cover images
- Ability to organize into shelves

# Parsing Metadata #

## ePub ##

Metadata is available in ePub file.

- ePub container is a zip archive. Unzip to access data.
- META-INF/container.xml has path to package document (usually content.opf)
- Package document contains lots of metadata about the book.
- If metadata is gathered from external sources, update package document.
- Package document can be expanded with additional elements, calibre adds new elements to it.
- Could potentially pass off some metadata finding responsibility to calibre.

## PDF ##

- PDF has data for title and author.
- No cover art (sometimes first page of PDF).
- Could potentially insert new image as first page of PDF.

# External Metadata Sources #

## isbndb.com ##

- API
- Author, publishing info
- Title search capability
- No cover images

## worldcat ##

- API
- API key may not be available to non-library sources
- Limited data

## Google Image Search ##

- API, use Google custom search for images
- Rate limited to 100 queries/day
- Search for images with "<book title> <author> cover"
- Grab first image or let user pick from search results
- Cache API response to avoid rate limit

## Calibre ##

- No API
- Calibre appears to update the metadata in the epub file, could just run them through Calibre and then save
- Check where Calibre gets their metadata and images from

# Open Questions #

- Are all ebooks stored in a single directory?
- How do we organize ebooks into shelves? Automatically or allow user to move them?
-- Could use folders as shelves.
-- Any modification of files would require web server running shell script. Check on what apps like sickbeard do.
--- Could have admin app like sickbeard which generates view only files for anyone to access
-- Can books be on more than one shelf?
- Need some kind of metadata cache for doing searching and sorting of the collection.

# Stages #

## 1 ##

- Create script to process all epub files in a directory.
- Generate a single metadata file and cache of cover images.
- Create basic view of books using metadata.

## 2 ##

- Simple admin interface to sort books into "shelf" folders.

## 3 ##

- Better viewing interface
- Ability to sort by date, author, series
- Search

## 4 ##

- Add external metadata capabilities

# Notes #

