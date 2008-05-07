<%inherit file="${context.get('c').layout or context.get('g').layout}"/>
<%def name="title()">${c.title or 'bad poems are good!'}</%def>

<style type="text/css">DIV#add_poem { display: none; }</style>
<% 
	from google.appengine.api import users
	user = users.get_current_user()
%>
% if user:
<a href="#" onclick="document.getElementById('add_poem').style.display = 'block'">+ Add a poem</a>
% endif
<%include file="/elements/new_poem.mako" />

% for p in c.poems:
<div class="poem">
	<h3>${p.title}</h3>
	<div class="author">by ${p.author.name}</div>
	<div class="meta">
		<div class="date">${p.created.strftime("%Y.%m.%d %H:%M")}</div>
		<div class="tags">
			% for tag in p.tags:
				${h.link_to(tag, h.url(controller="tags", action="show", id=tag))}
			% endfor
		</div>
		<div class="permalink">${h.link_to('(permalink)', h.url(action="show", id=p.key().id()))}</div>
	</div>
	<div class="content">
		${h.simple_format(p.content)}
	</div>
	<div class="clearall"></div>
</div>
% endfor