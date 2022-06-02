<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:media="http://search.yahoo.com/mrss/" 
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	version="2.0">
	<!-- declarem el namespace media, present al RSS, per poder fer-lo servir -->
	<xsl:template match="/">
		<html lang="ca">
			<head>
				<meta charset="UTF-8" />
				<meta http-equiv="X-UA-Compatible" content="IE=edge" />
				<meta name="viewport" content="width=device-width, initial-scale=1.0" />
				<link href='/static/css/style.css' rel='stylesheet' />
				<title>La Vanguardia</title>
			</head>
			<body>
				<h1>
					<xsl:value-of select="rss/channel/title" />
				</h1>
				<xsl:for-each select="rss/channel/item">
					<p>
						<a href="{link}" target="_blank"><xsl:value-of select="title" /></a>
					</p>
				</xsl:for-each>
			</body>
		</html>
	</xsl:template>
</xsl:stylesheet>
