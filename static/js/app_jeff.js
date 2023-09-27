// Hate Crimes in the US Code

d3.json("http://127.0.0.1:5000/data")
  .then(function (data) { 
    console.log(data); 
    })

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
