// SF Hate Crimes - Test Code

// DataSF portal
// SF Hate Crimes main page: https://data.sfgov.org/Public-Safety/Police-Department-Investigated-Hate-Crimes/huqr-9p9x
// API Docs: https://dev.socrata.com/foundry/data.sfgov.org/huqr-9p9x
const url = "https://data.sfgov.org/resource/huqr-9p9x.json?$where=occurence_month < '2023-07-01T00:00:00.000'"

// Fetch the JSON data and console log for review
d3.json(url).then(function(data) {
  console.log(data);
});