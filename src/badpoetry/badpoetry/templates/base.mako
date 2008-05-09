<%def name="title()"></%def>
<%def name="flash()">
	% if session.has_key('flash'):
		<div class="flash">${session['flash']}</div>
		<%
			del session['flash']
		 	session.save()
		%>
	% endif
</%def>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>Bad Poetry | ${self.title()}</title>
  ${h.stylesheet_link_tag('style.css')}
	${h.auto_discovery_link_tag("http://%s/rss" % (request.host))}
</head>
<body>
	<div id="header"><img src="/images/header.gif"></div>
	<div id="menu">
		${self.flash()}
		<div style="text-align: right">
		<% 
			from google.appengine.api import users
			user = users.get_current_user()
		%>
		% if user:
		${h.link_to('Logout', users.create_logout_url("/"))}
		% else:
		${h.link_to('Login', users.create_login_url("/"))}
		% endif
		</div>
		
		<div id="tag_selector">
			<h3>Filter by tag:</h3>
			<a href="/">(All tags)</a>&nbsp;&nbsp;&nbsp;
			% for tag in g.tags:
				${h.link_to(tag.tag, h.url(controller='tags', action='show', id=tag.tag))} <span class="count">(${tag.count})</span>
			% endfor
		</div>

		<div id="date_selector">
			<h3>Filter by date:</h3>
			<a href="/">(Any date)</a>
			<a href="/today">Today's Poems</a>
			<a href="/week">This Week's Poems</a>
			<a href="/month">This Month's Poems</a>
		</div>

	</div>

	${next.body()}
</body>
</html>
