---
layout: default
title: Journal
permalink: /blog/
---
<section class="wrap">
  <p class="eyebrow">Journal</p>
  <h1>Notes from the field</h1>
</section>

<ul class="post-list wrap">
  {% for post in site.posts %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%-d %b %Y" }}</time>
  </li>
  {% endfor %}
</ul>
