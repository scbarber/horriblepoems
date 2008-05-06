<%inherit file="${context.get('c').layout or context.get('g').layout}"/>
<%def name="title()">bad poems are good!</%def>

<%include file="/elements/new_poem.mako" />

% for p in c.poems:
<div class="poem">
	<h3>${p.title}</h3>
	<hr />
	<div class="meta">
		<div class="author"></div>
		<div class="date">${p.created.strftime("%Y.%m.%d %H:%M")}</div>
		<div class="tags">
			% for tag in p.tags:
				${h.link_to(tag, h.url(controller="tags", action="show", id=tag))}
			% endfor
		</div>
		<div class="permalink">${h.link_to('(permalink)', h.url(action="show", id=p.key()))}</div>
	</div>
	<div class="content">
		${h.simple_format(p.content)}
	</div>
	<div class="clearall"></div>
</div>
% endfor