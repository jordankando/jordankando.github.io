(() => {
  "use strict";
  const root = document.getElementById("gx-widget");
  if (!root) return;
  const status = document.getElementById("gx-status");
  const plot = document.getElementById("gx-plot");
  const controls = document.getElementById("gx-controls");
  const reset = document.getElementById("gx-reset");
  const defaults = [[0, 200, 0.3], [0.5, 200, 0.5], [0, 200, 0.7]];
  const specs = [["Height", -15, 15, 0.01], ["Curvature", 100, 1000, 10], ["Position", 0, 1, 0.01]];
  const inputs = [];
  let worker, ready = false, busy = false, pending = false, timer;
  function draw() {
    if (!ready) return;
    if (busy) { pending = true; return; }
    busy = true;
    pending = false;
    status.textContent = "Updating plot…";
    plot.setAttribute("aria-busy", "true");
    worker.postMessage({ type: "plot", parameters: inputs.map(row => row.map(input => Number(input.value))) });
  }
  defaults.forEach((values, phase) => {
    const field = document.createElement("fieldset");
    field.disabled = true;
    const legend = document.createElement("legend");
    legend.textContent = `Phase ${phase + 1}`;
    legend.style.color = ["green", "#a65e00", "purple"][phase];
    field.appendChild(legend);
    inputs.push(values.map((value, parameter) => {
      const [name, min, max, step] = specs[parameter];
      const label = document.createElement("label");
      const input = document.createElement("input");
      const output = document.createElement("output");
      input.type = "range";
      input.id = `gx-${phase}-${parameter}`;
      Object.assign(input, { min, max, step, value });
      label.htmlFor = input.id;
      label.textContent = name;
      output.htmlFor = input.id;
      output.value = value;
      label.appendChild(output);
      input.addEventListener("input", () => {
        output.value = input.value;
        clearTimeout(timer);
        timer = setTimeout(draw, 100);
      });
      field.append(label, input);
      return input;
    }));
    controls.appendChild(field);
  });
  reset.addEventListener("click", () => {
    inputs.forEach((row, p) => row.forEach((input, k) => {
      input.value = defaults[p][k];
      input.previousElementSibling.querySelector("output").value = input.value;
    }));
    clearTimeout(timer);
    draw();
  });
  function fail(error) {
    console.error("G-X widget:", error);
    ready = false;
    busy = false;
    controls.querySelectorAll("fieldset").forEach(field => { field.disabled = true; });
    reset.disabled = true;
    plot.setAttribute("aria-busy", "false");
    status.textContent = "The plot could not load or update. Please reload to retry, or open the original notebook below.";
    if (worker) worker.terminate();
  }
  try {
    worker = new Worker(root.dataset.worker);
    worker.onerror = fail;
    worker.onmessage = ({ data }) => {
      if (data.type === "status") {
        status.textContent = data.message;
      } else if (data.type === "ready") {
        ready = true;
        controls.querySelectorAll("fieldset").forEach(field => { field.disabled = false; });
        reset.disabled = false;
        draw();
      } else if (data.type === "plot") {
        busy = false;
        // SVG comes only from the local Matplotlib renderer, not user markup.
        plot.innerHTML = data.svg.slice(data.svg.indexOf("<svg"));
        plot.setAttribute("aria-busy", "false");
        status.textContent = "Adjust the sliders to update the plot.";
        if (pending) draw();
      } else if (data.type === "error") fail(data.message);
    };
    worker.postMessage({ type: "init" });
    window.addEventListener("pagehide", event => {
      if (!event.persisted) worker.terminate();
    });
  } catch (error) { fail(error); }
})();
