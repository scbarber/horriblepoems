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
	</div>

	${next.body()}
</body>
</html>
