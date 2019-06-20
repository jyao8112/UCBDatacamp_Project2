// function buildMetadata(sample) {
//   // Using `d3.json` to fetch the metadata for a sample
//   // console.log(sample)
//   d3.json(`/metadata/${sample}`).then(function(sampleData) {
//     console.log(sampleData);
    
//     // Using d3 to select the panel with id of `#sample-metadata`
//     var PANEL = d3.select("#sample-metadata");
    
//     // Using `.html("") to clear any existing metadata
//     PANEL.html("");
    
//     // Using `Object.entries` to add each key and value pair to the panel
//     // Using d3 to append new tags for each key-value in the metadata.
//     Object.entries(sampleData).forEach(([key, value]) => {
//       PANEL.append('h6').text(`${key}, ${value}`);
//     })
    
//     // BONUS: Build the Gauge Chart
//     // buildGauge(data.WFREQ);
    
    
      
//     })
//   }
  
// function buildCharts(sample) {
    
//     // @TODO: Use `d3.json` to fetch the sample data for the plots
    
//     // @TODO: Build a Bubble Chart using the sample data
    
//     // @TODO: Build a Pie Chart
//     // HINT: You will need to use slice() to grab the top 10 sample_values,
//     // otu_ids, and labels (10 each).
    
//     // console.log(sample)  
    // d3.json(`/yelpdata`).then(function (yelpData) {
    //   console.log();
      
    //   //Building Pie Chart
    //   var pieData = [{
    //     values: .slice(0,10),
    //     labels: .slice(0,10),
    //     type: 'pie'
    //   }];

    //   var pieLayout = {
    //     margin: {t: 0, l: 0}
    //   }

    //   Plotly.plot('pie', pieData, pieLayout); 
    // });
// }
//       const otu_ids = sampleData.otu_ids;
//       const otu_labels = sampleData.otu_labels;
//       const sample_values = sampleData.sample_values;

//       //Building Bubble chart
//       var bubbleData = [{
//         x: otu_ids,
//         y: sample_values,
//         text: otu_labels,
//         mode: 'markers',
//         marker: {
//           size: sample_values,
//           color: otu_ids,
//           colorscale: 'Earth'
//         }
//       }];      

//       var bubbleLayout = {
//         margin: { t: 0 },
//         hovermode: 'closest',
//         xaxis: {title: 'OTU ID'},
//       };

//       Plotly.plot('bubble', bubbleData, bubbleLayout);

//       
  
  
  // const defaultURL = "/metadata/<sample>";
  // d3.json(defaultURL).then(function (data) {
  //   var data = [data];
  //   var layout = { margin: { t: 30, b: 100 } };
  //   Plotly.plot("bar", data, layout);
  // });


// Creating map object
var myMap = L.map("map", {
  // center: [40.7, -73.95],
  center: [37.7749, -122.44],
  zoom: 13
});

// Adding tile layer to the map
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: "pk.eyJ1IjoianVubGluY2hlbiIsImEiOiJjandsZnF4eDkwMzV3NDFtY3Z0aHI0eDdmIn0.mTWkH9uMiPE1yQyEY1SAdQ"
}).addTo(myMap);

var tbody = d3.select("tbody");  

var foodtypeData;
function buildFullTable() {
  var categories = [];
  d3.json("/yelpdata").then((data) => {
    foodtypeData = data;
    buildTableByData(data);
    buildMapByData(data);
  });
}

var StoreIcon = L.icon({
  iconUrl: 'https://image.flaticon.com/icons/svg/1916/1916263.svg',
  iconSize: [38, 95],
  iconAnchor: [22, 94],
  popupAnchor: [-3, -76],
});
var OpenMeter = L.icon({
  iconUrl: 'https://image.flaticon.com/icons/svg/148/148767.svg',
  iconSize: [38, 95],
  iconAnchor: [22, 94],
  popupAnchor: [-3, -76],
});
var closeMeter = L.icon({
  iconUrl: 'https://image.flaticon.com/icons/svg/148/148766.svg',
  iconSize: [38, 95],
  iconAnchor: [22, 94],
  popupAnchor: [-3, -76],
});


//L.marker([50.505, 30.57], {icon: myIcon}).addTo(map);

var markers;
function buildMapByData(data) {
  if (markers) {
    myMap.removeLayer(markers);
  }
  markers = L.markerClusterGroup();

  data.forEach((business) => {
    // Add a new marker to the cluster group and bind a pop-up
    markers.addLayer(L.marker(business.coordinates, {icon: StoreIcon}).bindPopup(business.name + "</br>(Rating: " + business.rating + ")"+"</br>(Price: " + business.price + ")"));
  });

  myMap.addLayer(markers);
}

var meterMarkers;
function buildTableByData(data) {
  tbody.html("");
  data.forEach((food) => {
    // categories.push([food.name, food.category_title, food.price, food.rating]);
    var category = [food.name, food.category_title, food.price, food.rating];
    var row = tbody.append("tr");
    // row.attr("yelp-id", food.yelp_id);
    row.on('click',function() {
      var meterStatus
      d3.json("/meterloc").then((data) => {
        var filteredMeter = data.filter(row => row["yelp_id"] === food.yelp_id);
        var meters = filteredMeter[0];
        console.log(meters);
        // d3.json("http://api.sfpark.org/sfpark/rest/availabilityservice?lat="+meters.meter1[1]+"&"+"long="+meters.meter1[2]+"&radius=0.25&uom=mile&response=json",function(statusRes) {
        // var stationStatus = statusRes.AVL.TYPE;
        //   console.log("meterstatus"+stationStatu)
          
        if (meterMarkers) {
          myMap.removeLayer(meterMarkers)
        }
        
        var meterMarkers = L.markerClusterGroup();
        meterMarkers.addLayer(L.marker([meters.meter1[1], meters.meter1[2]]).bindPopup("meter1"));
        meterMarkers.addLayer(L.marker([meters.meter2[1], meters.meter2[2]]).bindPopup("meter2"));
        meterMarkers.addLayer(L.marker([meters.meter3[1], meters.meter3[2]]).bindPopup("meter3"));
        meterMarkers.addLayer(L.marker([meters.meter4[1], meters.meter4[2]]).bindPopup("meter4"));
        meterMarkers.addLayer(L.marker([meters.meter5[1], meters.meter5[2]]).bindPopup("meter5"));
        meterMarkers.addLayer(L.marker([meters.meter6[1], meters.meter6[2]]).bindPopup("meter6"));
        meterMarkers.addLayer(L.marker([meters.meter7[1], meters.meter7[2]]).bindPopup("meter7"));
        meterMarkers.addLayer(L.marker([meters.meter8[1], meters.meter8[2]]).bindPopup("meter8"));
        meterMarkers.addLayer(L.marker([meters.meter9[1], meters.meter9[2]]).bindPopup("meter9"));
        meterMarkers.addLayer(L.marker([meters.meter10[1], meters.meter10[2]]).bindPopup("meter10"));

        myMap.addLayer(meterMarkers);
        // var group = new L.featureGroup([marker1, marker2, marker3]);
        myMap.fitBounds(meterMarkers.getBounds());
      });

      row.attr("style", "background-color: green;");
    });

    // console.log(category);
    Object.values(category).forEach((value) => {
      var cell = row.append("td");
      cell.text(value);
    
     });
   });
}



function updateFilters() {
  var changedElement = d3.select(this).select("select");
  var filterValue = changedElement.property("value");
  var filterId = changedElement.attr("id");

  var filters = {};
  if (filterValue) {
    filters[filterId] = filterValue;
  }
  else {
    delete filters[filterId];
  }
  filterTable(filters);
}
buildFullTable();

function filterTable(filters) {
  let filteredData = foodtypeData;
  Object.entries(filters).forEach(([key, value]) => {
    filteredData = filteredData.filter(row => row[key] === value);
  });
  buildTableByData(filteredData);
  buildMapByData(filteredData);
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#foodtype");

  // Use the list of sample names to populate the select options
  d3.json("/foodtype").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    // buildCharts(firstSample);
    // buildMetadata(firstSample);
  });
}

function optionChanged(newValue) {
  // Fetch new data each time a new sample is selected
  // buildCharts(newSample);
  // buildMetadata(newSample);

  var filters = {"category_title": newValue};
  filterTable(filters);
}

// Initialize the dashboard
init();
// buildTable(foodtypeData);