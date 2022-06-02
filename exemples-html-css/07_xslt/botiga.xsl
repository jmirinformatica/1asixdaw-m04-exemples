<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <!-- aquesta linia afegeix el <!DOCTYPE html> -->
    <xsl:output method="html" doctype-system="about:legacy-compat" />

    <xsl:template match="/">
        <html lang="ca">
            <head>
                <!-- aneu en cura de tancar totes les etiquetes... som al món XML! -->
                <meta charset="UTF-8" />
                <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <link rel="stylesheet" type="text/css" href="style.css" />
                <title>Exemple de XSLT</title>
            </head>
            <body>
                <h2>Els meus bluerays</h2>
                <table>
                    <tr>
                        <th>Títol</th>
                        <th>Director</th>
                    </tr>
                    <xsl:for-each select="botiga/bluray">
                        <tr>
                            <td>
                                <xsl:value-of select="titol"/>
                            </td>
                            <td>
                                <xsl:value-of select="director"/>
                            </td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>