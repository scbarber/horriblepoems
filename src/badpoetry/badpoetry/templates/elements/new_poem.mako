<div id="add_poem" class="poem">
	${h.form(h.url(action='add'), method='post')}
	<div class="required">
		<label for="title">Title</label>
		${h.text_field('title')}
	</div>
	<div class="required">
		<label for="content">Poem</label>
		${h.text_area('content', '', size="40x20")}
	</div>
	<div class="optional">
		<label for="tags">Tags <em style="font-weight: normal">(separated by commas)</em></label>
		${h.text_field('tags', autocomplete="off")}
		<div id="tag_suggestion" class="autocomplete" style="display: none"></div>
	</div>
	<div class="submit">${h.submit('Add some bad poetry')}</div>
	${h.end_form()}
</div>
<script type="text/javascript">new Ajax.Autocompleter("tags", "tag_suggestion", "/tags/suggest", {paramName: "tag", tokens: ', '});</script>