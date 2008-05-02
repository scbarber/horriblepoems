<%inherit file="${context.get('c').layout or context.get('g').layout}"/>
<%def name="title()">bad poems are good!</%def>

<%include file="/elements/new_poem.mako" />