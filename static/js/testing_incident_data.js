// SF Hate Crimes - Test Code

// DataSF portal
// SF Hate Crimes main page: https://data.sfgov.org/Public-Safety/Police-Department-Investigated-Hate-Crimes/huqr-9p9x
// API Docs: https://dev.socrata.com/foundry/data.sfgov.org/huqr-9p9x
// const url = "https://data.sfgov.org/resource/huqr-9p9x.json?$where=occurence_month < '2023-07-01T00:00:00.000'"

// Police indident reports - checking Jan 2022 to see if hate crimes are in this dataset
const url = "https://data.sfgov.org/resource/wg3w-h783.json?$where=incident_date between '2022-01-01T00:00:00.000' and '2022-02-01T00:00:00.000'";

// Fetch the JSON data and console log for review
d3.json(url).then(function(data) {
  console.log('Data: ', data);
  
  // Get categories for 
  categories = getIncidentCategories(data);
  console.log('Incident Categories: ', categories[0]);
  console.log('Incident Subcategories: ', categories[1]);

});

function getIncidentCategories(incidents) {
  let categories = [];
  let subCategories = []
  for (let i=0; i<incidents.length; i++) {
    let category = incidents[i].incident_category;
    let subCategory = incidents[i].incident_subcategory;
    if (categories.includes(category) === false) {
      categories.push(category);
    };
    if (subCategories.includes(subCategory) === false) {
      subCategories.push(subCategory);
    };
        
  };

  return [categories, subCategories];
}