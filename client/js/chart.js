function renderChart(timeData) {
  const ctx = document.getElementById('myChart');
  const dataMap = timeData.map((datum) => {
    return {
      x: datum.time,
      y: datum.f,
    }
  })
  new Chart(ctx, {
    type: 'line',
    data: dataMap
  });
}
