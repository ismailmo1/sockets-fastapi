const btn = document.getElementById("btn");

var ws = new WebSocket("ws://localhost:8000/ws");
const chartData = {
  x: [],
  y: [],
  type: "scatter",
};
Plotly.newPlot("lineChart", [chartData]);

btn.addEventListener("click", () => {
  const streamRate = document.getElementById("streamRate").value;
  const numPoints = document.getElementById("numPoints").value;
  ws.send(JSON.stringify({ streamRate, numPoints }));
});
ws.onmessage = function (event) {
  const data = JSON.parse(event.data);
  const { temp } = data;
  console.log(temp, data.timestamp);
  Plotly.extendTraces(
    "lineChart",
    {
      y: [[temp]],
      x: [[data.timestamp]],
    },
    [0]
  );
};
