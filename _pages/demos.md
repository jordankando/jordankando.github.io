---
layout: archive
permalink: /demos/
title: "Demos"
author_profile: true
---

{% include base_path %}

Coding project demos and descriptions can be found here in blog format.

All Jupyter Notebook demos can be executed from browser at this [link.](https://jordankando.github.io/code-demos/)

{% for post in site.demos %}
  {% include archive-single.html %}
{% endfor %}
