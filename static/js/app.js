d3.json("http://127.0.0.1:5000/bias")
  .then(function(data) {
    console.log(data);     
  })
  .catch(function (error) {
    console.error("Error loading JSON data:", error);
  });

d3.json("http://127.0.0.1:5000/matt")
  .then(function (data) {
    console.log(data);

    // Create a set to store unique state names
    const uniqueStateNames = new Set();

    // Populate the select options with state names
    const selectElement = d3.select("#selDataset");

    // Iterate through the state data
    data.state_data.forEach(state_dataEntry => {
      const stateName = state_dataEntry.state;

      // Check if the state name is not already in the set
      if (!uniqueStateNames.has(stateName)) {
        selectElement.append("option").attr("value", stateName).text(stateName);
        // Add the state name to the set to mark it as encountered
        uniqueStateNames.add(stateName);
      }
    });

    // Set up an event listener for the select element change event
    selectElement.on("change", function () {
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
  const filteredData = stateData.filter(entry => entry.state === selectedState);

  // Group data by bias category
  const groupedData = {};

  filteredData.forEach(entry => {
    if (!groupedData[entry.category]) {
      groupedData[entry.category] = {
        x: [],
        y: [],
        mode: 'lines+markers',
        name: entry.category,
      };
    }
    groupedData[entry.category].x.push(entry.year);
    groupedData[entry.category].y.push(entry.count);
  });

  // Sort data within each bias group by year
  Object.values(groupedData).forEach(group => {
    const sortedIndices = group.x.map((_, i) => i).sort((a, b) => group.x[a] - group.x[b]);
    group.x = sortedIndices.map(i => group.x[i]);
    group.y = sortedIndices.map(i => group.y[i]);
  });

  const chartData = Object.values(groupedData);

  const layout = {
    title: "Hate Crimes by Bias Category Over Time",
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
    console.log(data);
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
  
d3.json("http://127.0.0.1:5000/top10Data")
  .then(function (data) { 
    console.log('Top 10 Data', data);
    
    // Store JSON data in separate variables
    let states = data.states;
    let years = data.years;
    let chart_data = data.data;
    
    // Log first row of data in variables for review
    console.log('States:', states);
    console.log('Years:', years);
    console.log('First year (2009):', chart_data[0]);
    
    const selectYear = d3.select('#selYear');
    let initial_year = 2021;

    createYearDropDown(years);
    createTop10Chart(chart_data[initial_year - 2009]);
    
    // Set up an event listener for the select element change event
    selectYear.on("change", function() {
      let year = this.value; // Get the selected year from the dropdown
      console.log(year);
      createTop10Chart(chart_data[year - 2009]);
    });

  });

function yearChanged(year) {
  
  let new_chart_data = chart_data[year - 2009];
  createTop10Chart(new_chart_data);
}

function createYearDropDown(years) {
    
  // Loop through all names/IDs and add drop down menu option for each test subject
  for(let i=0; i<years.length; i++) {
    year = years[i]; 
    // Add option elementference for updating charts/info 
    d3.select('#selYear').append('option').text(year).attr('value', year);
  };
}
    
function createTop10Chart(info) {

  let states = info.states;
  let incidents = info.incidents;
  let incident_rate = info.incident_rate;
  
  states = states.slice(0, 10).reverse();
  incidents = incidents.slice(0, 10).reverse();
  incident_rate = incident_rate.slice(0, 10).reverse();

  // Create data variable for plotting charts
  let data = [{
    x: incidents,
    y: states,
    text: incident_rate,
    type: 'bar',
    orientation: 'h'
  }];
    
  // Log data for review
  console.log('Initial Bar Chart Data:', data)
       
  let layout = {
    title: 'Top 10 States with the Most Incidents',
    height: 425,
    width: 500,
    margin: {
      l: 120, // Create gap between demographic info and chart,
      t: 0, // Align chart with top of subject drop down
      b: 25 // Reduce gap with bubble chart
    }
  };
    
  // Plot chart
  Plotly.newPlot('top10bar', data, layout);
    
}

d3.json("http://127.0.0.1:5000/state_offense")
    .then(function(data) {
        const uniqueStates = new Set();
        const uniqueYears = new Set();
        data.state_offense_data.forEach(entry => {
            uniqueStates.add(entry.state_name);
            uniqueYears.add(entry.data_year);
        });
        const stateFilter = d3.select("#stateFilter");
        uniqueStates.forEach(state => {
            stateFilter.append("option").attr("value", state).text(state);
        });
        const yearFilter = d3.select("#yearFilter");
        uniqueYears.forEach(year => {
            yearFilter.append("option").attr("value", year).text(year);
        });
        renderStateOffenseChart(data, "All", "All");
        stateFilter.on("change", function() {
            const selectedState = this.value;
            const selectedYear = yearFilter.node().value;
            renderStateOffenseChart(data, selectedState, selectedYear);
        });
        yearFilter.on("change", function() {
            const selectedYear = this.value;
            const selectedState = stateFilter.node().value;
            renderStateOffenseChart(data, selectedState, selectedYear);
        });
    })
    .catch(function(error) {
        console.error("Error loading JSON data:", error);
    });
​
function renderStateOffenseChart(data, selectedState, selectedYear) {
    let filteredData = data.state_offense_data;
    if (selectedState !== "All") {
        filteredData = filteredData.filter(entry => entry.state_name === selectedState);
    }
    if (selectedYear !== "All") {
        filteredData = filteredData.filter(entry => entry.data_year === parseInt(selectedYear));
    }
    const offenseCount = {};
    filteredData.forEach(entry => {
        if (!offenseCount[entry.offense_name]) {
            offenseCount[entry.offense_name] = 0;
        }
        offenseCount[entry.offense_name] += entry.count;
    });
    const sortedOffenses = Object.keys(offenseCount).sort((a, b) => offenseCount[b] - offenseCount[a]).slice(0, 10);
    const topOffenseCounts = sortedOffenses.map(offense => offenseCount[offense]);
    const chartData = [{
        type: 'bar',
        x: topOffenseCounts,
        y: sortedOffenses,
        orientation: 'h'
    }];
    const layout = {
        title: `Top 10 Hate Crimes by Offense in ${selectedState} for ${selectedYear}`,
        yaxis: { title: "Offense Name", automargin: true },
        xaxis: { title: "Count" },
        margin: { l: 250 }
    };
    Plotly.newPlot("chart4", chartData, layout);
}
