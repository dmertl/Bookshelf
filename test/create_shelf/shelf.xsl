<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:template match="/">
        <html>
            <head>
                <title>Bookshelf</title>
            </head>
            <body>
                <ul class="bookshelf">
                    <xsl:for-each select="shelf/book">
                        <li class="book">
                            <img src="" alt="" />
                            <xsl:value-of select="title"/>
                        </li>
                    </xsl:for-each>
                </ul>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>