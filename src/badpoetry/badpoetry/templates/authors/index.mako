<%inherit file="${context.get('c').layout or context.get('g').layout}"/>
<%def name="title()">all our authors</%def>

<h1>All our authors:</h1>

<ul>
% for author in c.authors:
	<li>${h.link_to(author.user.nickname(), h.url(controller='poems', action='author', id=author.key()))} <span class="count">(${author.poem_count})</span></li>
% endfor
</ul>