<%
	scores = [
		["", None],
		["THAT'S NOT BAD!  THAT'S GOOD POETRY!", -2],
		["Heh.  I enjoyed that one.", -1],
		["Meh.", 0],
		["Ow.  I hurt.", 1],
		["MY EYES!  OH MY POOR EYES!", 2]]
%>
<div class="rating">
	<select name="score" onchange="new Ajax.Updater('score-${c.poem.key()}', '${h.url_for(controller="poems", action="score", id=c.poem.key())}', { parameters: { score: $F(this)}}); $('rating'-${c.poem.key()}).toggle()">
	${h.options_for_select(scores, c.score)}
	</select>
	<span class="ajax_link" onclick="$('rating-${c.poem.key()}').hide()">cancel</span>
</div>