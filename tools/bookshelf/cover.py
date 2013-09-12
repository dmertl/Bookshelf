class Cover:
    def __init__(self, href, data, media_type):
        self.href = href
        self.data = data
        self.mediaType = media_type

    def write(self, path):
        fh = open(path, 'w+')
        fh.write(self.data)
        fh.close()
