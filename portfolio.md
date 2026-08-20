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
  </div>
</section>
