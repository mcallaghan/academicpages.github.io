---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---


{% include base_path %}

{% if author.googlescholar %}
  A full and up-to-date list of articles can be found on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}


<ol>{% for post in site.publications reversed %}
  {% include archive-single-cv.html %}
{% endfor %}</ol>
