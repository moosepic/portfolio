---
layout: default
title: Journal
permalink: /blog/
---
<section class="wrap narrow">
  <p class="eyebrow">Journal</p>
  <h1>Notes from the field</h1>

  <ul class="post-list">
    {% for post in site.posts %}
    <li>
      <div class="post-list-heading">
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
        <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%-d %b %Y" }}</time>
      </div>
      {% assign excerpt_text = post.excerpt | strip_html | strip_newlines | strip %}
      {% if excerpt_text != empty %}
      <p class="post-list-excerpt">{{ excerpt_text | truncate: 100 }}</p>
      {% endif %}
    </li>
    {% endfor %}
  </ul>
</section>
