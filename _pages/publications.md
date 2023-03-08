---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

Most of my planetary science work is best accessed right now in the form of LPSC-style conference abstracts. Check out the "Talks" section above for details.


{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
