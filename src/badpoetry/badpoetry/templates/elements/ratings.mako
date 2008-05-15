<%
	scores = {
		-2:"THAT'S NOT BAD!  THAT'S GOOD POETRY!",
		-1:"Heh.  I enjoyed that one.",
		0:"Meh.",
		1:"Ow.  I hurt.",
		2:"MY EYES!  OH MY POOR EYES!"}
	scores = [
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
</div>