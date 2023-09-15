// Hate Crimes in the US - Test Code


// FBI Hate Crimes Data Explorer: https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/explorer/crime/hate-crime
// API Docs: https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/docApi



api_key = 'xZxFWvOLGhsTFKV76mlJpVfR9xrG8hwE118gesyc';
const baseUrl = 'https://api.usa.gov/crime/fbi/cde/hate-crime/national/';
const baseParams = '?year=2021&API_KEY=' + api_key;
const categories = ['bias_incident', 'location', 'offense', 'offender_race', 'offender_ethcity', 'victim_type']; 

let i = 1; // Use to get info on one of the categories above
const url = baseUrl + categories[i] + baseParams;

// Fetch the JSON data and console log for review
d3.json(url).then(function(data) {
  console.log(categories[i], data.keys);
});