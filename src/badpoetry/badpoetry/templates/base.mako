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
	${h.javascript_include_tag('prototype')}
	${h.javascript_include_tag('scriptaculous')}
</head>
<body>
	<div id="header"><img src="/images/header.gif"></div>
	<div id="menu">
		<div style="float: left"><a href="/">[home]</a></div>
		${self.flash()}
		<div id="user_menu">
		<% 
			from google.appengine.api import users
			user = users.get_current_user()
		%>
		% if user:
			Welcome ${user.nickname()}! || 
			<a href="/poems/mine">My Poems</a> | 
			<a href="/poems/favourites">My Favs</a> | 
			${h.link_to('Logout', users.create_logout_url("/"))}
		% else:
			${h.link_to('Login', users.create_login_url("/"))}
		% endif
		</div>
		
		<div id="tag_selector">
			<h3>Top 10 Tags:</h3>
			<a href="/tags/" title="List of Tags">[list]</a>
			% for tag in g.tags:
				${h.link_to(tag.tag, h.url(controller='tags', action='show', id=tag.tag))} <span class="count">(${tag.count})</span>
			% endfor
		</div>

		<div id="author_selector">
			<h3>Top 10 Authors (by quantity):</h3>
			<a href="/authors/" title="List of Authors">[list]</a>
			% for author in g.authors:
				${h.link_to(author.user.nickname(), h.url(controller='poems', action='author', id=author.key()))} <span class="count">(${author.poem_count})</span>
			% endfor
		</div>

		<div id="date_selector">
			<h3>Filter by date:</h3>
			<a href="/today">Today's Poems</a> |
			<a href="/week">This Week's Poems</a> |
			<a href="/month">This Month's Poems</a>
		</div>

	</div>

	${next.body()}
	
	<div id="footer">
		made in collaboration with <em>purple monkey dishwasher</em> and <em>vintage electricity</em><br/>
		${h.link_to('<img src="/images/rss.png" width="38" height="39" border="0"/>', "http://%s/rss" % (request.host))}
	</div>
</body>
</html>
