<%def name="title()"></%def>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>Bad Poetry | ${self.title()}</title>
  ${h.stylesheet_link_tag('style.css')}
</head>
<body>
	<div id="header"><img src="/images/header.gif"></div>
	<div id="workingheader">
		<div id="tag_selector">
		<h3>Filter by tag:</h3>
		${h.link_to('(All tags)', h.url(controller='poems', action='index'))}&nbsp;&nbsp;&nbsp;
		% for tag in g.tags:
			${h.link_to(tag.tag, h.url(controller='tags', action='show', id=tag.tag))} <span class="count">(${tag.count})</span>
		% endfor
		</div>
	</div>

	${next.body()}
</body>
</html>
