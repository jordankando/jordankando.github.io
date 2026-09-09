---
title: 'Interactive G-X Phase Diagrams (ERTH 602 Final Project)'
date: 2023-04-30
permalink: /gx-diagrams/
collection: demos

---

I wrote this code to explore how different phases' Gibbs free energy (G) curves interact to create stable phase equilibria.

Adjust the sliders below to change the height, curvature, and position of three parabolic G curves. Black lines show common tangents selected by the notebook's solver; dashed lines mark their contact compositions. Each curve has the form G = curvature × (X₂ − position)² + height.

{% include base_path %}
<link rel="stylesheet" href="{{ base_path }}/assets/gx-diagrams/widget.css">
<div id="gx-widget" data-worker="{{ base_path }}/assets/gx-diagrams/worker.js">
  <p id="gx-status" role="status" aria-live="polite">Loading Python and plotting libraries. The first load may take a minute.</p>
  <div id="gx-plot" role="img" aria-label="Gibbs free energy curves and common tangents for three phases" aria-busy="true"></div>
  <div id="gx-controls"></div>
  <button id="gx-reset" type="button" disabled>Reset sliders</button>
  <noscript>This interactive plot requires JavaScript. You can use the original notebook linked below instead.</noscript>
</div>
<script src="{{ base_path }}/assets/gx-diagrams/widget.js" defer></script>

[Open the original Jupyter notebook](https://jordankando.github.io/code-demos/lab/index.html?path=interactive_GX_phase_diagrams.ipynb) · [View the Python plotting code]({{ base_path }}/assets/gx-diagrams/plot.py)
