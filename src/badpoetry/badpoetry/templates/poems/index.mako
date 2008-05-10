<%inherit file="${context.get('c').layout or context.get('g').layout}"/>
<%def name="title()">${c.title or 'bad poems are good!'}</%def>
<%def name="pager()">
% if hasattr(c.poems, 'pager'):
<div class="pager">
	${c.poems.pager(format='$link_previous ~2~ $link_next', symbol_previous="&laquo; Previous", symbol_next="Next &raquo;")}
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

% if c.title:
<h1 class="title">${c.title.capitalize()}</h1>
% endif

<style type="text/css">DIV#add_poem { display: none; }</style>
% if c.user:
<div id="add"><span class="add" onclick="if($('add_poem').style.display == 'block') $('add_poem').style.display = 'none'; else $('add_poem').style.display = 'block';">+ Add a poem</span></div>
% endif
<%include file="/elements/new_poem.mako" />

${pager()}

% for p in c.poems:
<div class="poem">
	<h3>${p.title}</h3>
	<div class="author">by ${p.author.nickname()}</div>
	<div class="meta">
		% if c.user:
			<%
				if c.user in p.favourites: img = "fav.png"
				else:	img = "no_fav.png"
			%>
			<img style="cursor: pointer" class="favourite" src="/images/${img}" onclick="new Ajax.Request('${h.url_for(controller="poems", action="favourite", id=p.key())}'); toggle_fav(this);">
		% endif
		<div class="date">${p.created.strftime("%Y.%m.%d %H:%M")}</div>
		<div class="tags">
			${', '.join([h.link_to(tag, h.url(controller="tags", action="show", id=tag)) for tag in p.tags])}
		</div>
		<div class="permalink">
			${h.link_to('(permalink)', h.url(controller="poems", action="show", id=p.key()))}
			% if c.user == p.author:
			<p style="text-align: center">
			${h.link_to('edit', h.url(controller="poems", action="edit", id=p.key()))}
			| ${h.link_to('delete', h.url(controller="poems", action="delete", id=p.key()), confirm="Are you sure?")}
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