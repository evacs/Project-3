// Hate Crimes in the US Code

d3.json("http://127.0.0.1:5000/data")
  .then(function (data) { 
    console.log(data); 
    })

d3.json("http://127.0.0.1:5000/categories")
  .then(function(data) {
    console.log(data);
  })
  .catch(function (error) {
    console.error("Error loading JSON data:", error);
  });
  
  
  // Extract data for the chart
    
    const bias = data.bias;
    const categories = data.bias_categories;
    const labels = []  
    function init() {
      let data = [{
        values: categories,
        labels: categories,
        type: "pie"
      }];
    
      let layout = {
        height: 600,
        width: 800
      };
    
      Plotly.newPlot("pie", data, layout);
    }
