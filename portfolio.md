---
layout: default
title: Portfolio
permalink: /portfolio/
---
<section class="wrap">
  <p class="eyebrow">Portfolio</p>
  <h1>Galleries</h1>

  <div class="gallery-grid">
    {% assign galleries = site.galleries | sort: 'order' %}
    {% for g in galleries %}
    <a class="gallery-card" href="{{ g.url | relative_url }}">
      <span class="cover" style="background-image: url('{{ g.cover | relative_url }}');"></span>
      <span class="card-label">{{ g.title }} <span class="card-count">— {{ g.images.size }}</span></span>
    </a>
    {% endfor %}

    {% assign groups = site.data.gallery_groups | sort: 'order' %}
    {% for group in groups %}
    {% assign group_count = site.galleries | where: "group", group.slug | size %}
    <a class="gallery-card" href="{{ '/portfolio/' | append: group.slug | append: '/' | relative_url }}">
      <span class="cover" style="background-image: url('{{ group.cover | relative_url }}');"></span>
      <span class="card-label">{{ group.title }} <span class="card-count">— {{ group_count }} galleries</span></span>
    </a>
    {% endfor %}
  </div>
</section>
