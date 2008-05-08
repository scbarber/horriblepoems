<%inherit file="${context.get('c').layout or context.get('g').layout}"/>
<%def name="title()">${c.title or 'bad poems are good!'}</%def>
<%def name="pager()">
% if hasattr(c.poems, 'pager'):
<div class="pager">
	${c.poems.pager('~2~')}
</div>
%endif
</%def>

<style type="text/css">DIV#add_poem { display: none; }</style>
% if c.user:
<div id="add"><a href="#" class="add" onclick="document.getElementById('add_poem').style.display = 'block'">+ Add a poem</a></div>
% endif
<%include file="/elements/new_poem.mako" />

${pager()}

% for p in c.poems:
<div class="poem">
	<h3>${p.title}</h3>
	<div class="author">by ${p.author.nickname()}</div>
	<div class="meta">
		<div class="date">${p.created.strftime("%Y.%m.%d %H:%M")}</div>
		<div class="tags">
			% for tag in p.tags:
				${h.link_to(tag, h.url(controller="tags", action="show", id=tag))}
			% endfor
		</div>
		<div class="permalink">
			${h.link_to('(permalink)', h.url(action="show", id=p.key()))}
			% if c.user == p.author:
			<p style="text-align: center">
			${h.link_to('edit', h.url(action="edit", id=p.key()))}
			| ${h.link_to('delete', h.url(action="delete", id=p.key()), confirm="Are you sure?")}
			</p>
			% endif
		</div>
	</div>
	<div class="content">
		${h.simple_format(p.content)}
	</div>
	<div class="clearall"></div>
</div>
% endfor

${pager()}