<%inherit file="${context.get('c').layout or context.get('g').layout}"/>
<%def name="title()">editing ${c.title}</%def>

<h2>Editing | ${c.title}</h2>
<div id="add_poem" class="poem">
	${h.form(h.url(action='update', id=c.poem.key()), method='post')}
	<div class="required">
		<label for="title">Title</label>
		${h.text_field('title', c.poem.title)}
	</div>
	<div class="required">
		<label for="content">Poem</label>
		${h.text_area('content', c.poem.content, size="40x20")}
	</div>
	<div class="optional">
		<label for="tags">Tags</label>
		${h.text_field('tags', " ".join(c.poem.tags))}
	</div>
	<div class="submit">${h.submit('Update')}</div>
	${h.end_form()}
</div>