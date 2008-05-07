<%inherit file="${context.get('c').layout or context.get('g').layout}"/>
<%def name="title()">all our tags</%def>

<h1>All our tags:</h1>

<ul>
% for tag in c.tags:
	<li>${h.link_to(tag.tag, h.url(controller='tags', action='show', id=tag.tag))} <span class="count">(${tag.count})</span></li>
% endfor
</ul>