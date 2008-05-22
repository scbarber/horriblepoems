<?xml version="1.0"?>
<% from time import gmtime, strftime %>
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">
	<channel>
		<title>Bad Poetry</title>
		<link>${request.scheme}://${request.host}</link>
		<description>Bad Poetry</description>
		<language>en-us</language>
		<pubDate>${strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())}</pubDate>
		<lastBuildDate>${strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())}</lastBuildDate>

% for p in c.poems:
		<item>
			<title>${p.title}</title>
			<link>${request.scheme}://${request.host}${h.url_for(controller="poems", action="show", id=p.key())}</link>
			<description><![CDATA[${h.simple_format(p.content)}]]></description>
			<dc:creator>${p.author.nickname()}</dc:creator>
			<dc:subject>${' '.join(p.tags)}</dc:subject>
			<pubDate>${p.created.strftime("%a, %d %b %Y %H:%M:%S")}</pubDate>
			<guid>${request.scheme}://${request.host}${h.url_for(controller="poems", action="show", id=p.key())}</guid>
		</item>
% endfor
	</channel>
</rss>		