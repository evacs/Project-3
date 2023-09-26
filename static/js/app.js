// Hate Crimes in the US Code

d3.json("http://127.0.0.1:5000/matt")
  .then(function (data) {
    console.log(data);
    // Create a set to store unique state names
    const uniqueStateNames = new Set();

    // Populate the select options with state names
    const selectElement = d3.select("#selDataset");

    // Iterate through the state data
    data.state_data.forEach(state_dataEntry => {
      const stateName = state_dataEntry.state_name;

      // Check if the state name is not already in the set
      if (!uniqueStateNames.has(stateName)) {
        selectElement.append("option").attr("value", stateName).text(stateName);
        // Add the state name to the set to mark it as encountered
        uniqueStateNames.add(stateName);
      }
    });
    
    // Set up an event listener for the select element change event
    selectElement.on("change", function() {
      let selectedState = this.value; // Get the selected state from the dropdown
      createLineChart(selectedState, data.state_data);
    });

    // Get the initial state (e.g., "Alabama") for the line chart
    let selectedState = "Alabama";
    createLineChart(selectedState, data.state_data);
  });

// Function to create the line chart
function createLineChart(selectedState, stateData) {
  // Filter the state data for the selected state
  const filteredData = stateData.filter(entry => entry.state_name === selectedState);

  // Group data by bias_desc
  const groupedData = {};

  filteredData.forEach(entry => {
    if (!groupedData[entry.bias_desc]) {
      groupedData[entry.bias_desc] = {
        x: [],
        y: [],
        mode: 'lines+markers',
        name: entry.bias_desc,
      };
    }
    groupedData[entry.bias_desc].x.push(entry.data_year);
    groupedData[entry.bias_desc].y.push(entry.count);
  });

  // Sort data within each bias_desc group by data_year
  Object.values(groupedData).forEach(group => {
    const sortedIndices = group.x.map((_, i) => i).sort((a, b) => group.x[a] - group.x[b]);
    group.x = sortedIndices.map(i => group.x[i]);
    group.y = sortedIndices.map(i => group.y[i]);
  });

  const chartData = Object.values(groupedData);

  const layout = {
    title: "Hate Crimes by Bias Over Time",
    xaxis: { title: "Year" },
    yaxis: { title: "Incident Count" },
    height: 600,
    width: 1200,
  };

  // Create the line chart using Plotly
  Plotly.newPlot("chart1", chartData, layout);
}


d3.json("http://127.0.0.1:5000/time")
  .then(function(data) {
    console.log(data.count);
    time_data = data;
    timelineChart(time_data);
  })
  .catch(function (error) {
    console.error("Error loading JSON data:", error);
  });



  function timelineChart(timeData) {
    // Extract data for the chart
    const data = timeData.time_data;
    const years = data.map(item => item.data_year);
    const counts = data.map(item => item.count);
    
    // Create a trace for the line chart
    const trace = {
      x: years,
      y: counts,
      type: 'line',
      mode: 'lines+markers', // Show markers on data points
      marker: {
        color: 'blue' // Customize line color
      }
    };
  
    // Specify the layout options for the chart
    const layout = {
      title: "Total Hate Crimes Over Time",
      xaxis: { title: "Year" },
      yaxis: { title: "Incident Count" },
    };
  
    // Create a data array with the trace
    const plotData = [trace];
  
    // Render the line chart in the specified container
    Plotly.newPlot('chart2', plotData, layout);
  }