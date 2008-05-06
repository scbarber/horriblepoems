<%inherit file="${context.get('c').layout or context.get('g').layout}"/>
<%def name="title()">add a new poem</%def>

<h2>Add a New Poem</h2>
<%include file="/elements/new_poem.mako" />
