/* Keep Python and the numerical solver off the page's UI thread. */
const runtimeURL = "https://cdn.jsdelivr.net/pyodide/v314.0.6/full/";
let python;
self.onmessage = async ({ data }) => {
  try {
    if (data.type === "init") {
      const { loadPyodide } = await import(runtimeURL + "pyodide.mjs");
      python = await loadPyodide({ indexURL: runtimeURL });
      self.postMessage({ type: "status", message: "Loading NumPy, SciPy, and Matplotlib…" });
      await python.loadPackage(["numpy", "scipy", "matplotlib"]);
      self.postMessage({ type: "status", message: "Preparing the plot…" });
      const response = await fetch(new URL("plot.py", self.location.href));
      if (!response.ok) throw new Error("Could not load plotting code");
      await python.runPythonAsync(await response.text());
      self.postMessage({ type: "ready" });
    } else if (data.type === "plot") {
      python.globals.set("parameters_json", JSON.stringify(data.parameters));
      const svg = python.runPython("import json\nrender_plot(json.loads(parameters_json))");
      self.postMessage({ type: "plot", svg });
    }
  } catch (error) {
    self.postMessage({ type: "error", message: String(error) });
  }
};
