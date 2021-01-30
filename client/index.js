const currentState = fetchCurrentState();

const app = new Vue({
  el: '#app',
  data: {
    lowerBound: currentState.lower_temp_bound || {},
    upperBound: currentState.upper_temp_bound || {},
  }
})

renderChart(currentState.temperatures)
