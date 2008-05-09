<%inherit file="${context.get('c').layout or context.get('g').layout}"/>
<%def name="title()">${c.title or 'bad poems are good!'}</%def>
<%def name="pager()">
% if hasattr(c.poems, 'pager'):
<div class="pager">
	${c.poems.pager('~2~')}
</div>
%endif
</%def>

<script type="text/javascript">
	function toggle_fav(img) {
		if(img.src.match("no_"))
			img.src = img.src.replace(/no_/, "");
		else
			img.src = img.src.replace(/fav/, "no_fav");
	}
</script>

<style type="text/css">DIV#add_poem { display: none; }</style>
% if c.user:
<div id="add"><a href="#" class="add" onclick="if($('add_poem').style.display == 'block') $('add_poem').style.display = 'none'; else $('add_poem').style.display = 'block';">+ Add a poem</a></div>
% endif
<%include file="/elements/new_poem.mako" />

${pager()}

% for p in c.poems:
<div class="poem">
	% if c.user:
		<%
			if c.user in p.favourites: img = "fav.png"
			else:	img = "no_fav.png"
		%>
		<img style="cursor: pointer" class="favourite" src="/images/${img}" onclick="new Ajax.Request('${h.url_for(action="favourite", id=p.key())}'); toggle_fav(this);">
	% endif
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