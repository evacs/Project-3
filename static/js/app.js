// Hate Crimes in the US Code

d3.json("http://127.0.0.1:5000/data")
  .then(function (data) {
    console.log(data); 
    })

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
      
      // Get the initial state (e.g., "Alabama") for the line chart
      const initialState = "Alabama";
      createLineChart(initialState, data.state_data);
    });
  
  // Function to create the line chart
  function createLineChart(initialState, stateData) {
    // Filter the state data for the selected state
    const filteredData = stateData.filter(entry => entry.state_name === initialState);
  
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
  
    const chartData = Object.values(groupedData);
  
    const layout = {
      title: "Hate Crimes by Bias Over Time",
      xaxis: { title: "Year" },
      yaxis: { title: "Count" },
      height: 600,
      width: 800,
    };
  
    // Create the line chart using Plotly
    Plotly.newPlot("line", chartData, layout);
  }