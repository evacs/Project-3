// Hate Crimes in the US Code

d3.json("http://127.0.0.1:5000/data")
  .then(function (data) { 
    console.log(data); 
    })

d3.json("http://127.0.0.1:5000/top10Data")
  .then(function (data) { 
    console.log(data); 
    })
  
