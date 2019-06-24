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
  id: "mapbox.streets-satellite",
  accessToken: API_KEY
}).addTo(myMap);

// Store API query variables
// var baseURL = "https://data.cityofnewyork.us/resource/fhrw-4uyv.json?";
// var date = "$where=created_date between'2016-01-10T12:00:00' and '2017-01-01T14:00:00'";
// var complaint = "&complaint_type=Rodent";
// var limit = "&$limit=10000";


// var url = baseURL + date + complaint + limit;
var url = "/yelpdata"
// // Grab the data with d3
d3.json(url, function(response) {
console.log(response)
var markers = L.markerClusterGroup();

//   Loop through data
for (var i = 0; i < response.length; i++) {

//   Set the data location property to a variable
var latitude = response[i].latitude;
var longitude = response[i].longitude;
console.log(latitude,longitude)
      // Add a new marker to the cluster group and bind a pop-up
      markers.addLayer(L.marker(response[i].coordinates)
      .bindPopup(response[i].name));  
  
}
    // Add our marker cluster layer to the map
    myMap.addLayer(markers);
});


// Check for location property
      //  if (coordinates) {

//       // Add a new marker to the cluster group and bind a pop-up
      //  markers.addLayer(L.marker(response[i].coordinates)
      //    .bindPopup(response[i].name));
//     }

//   }

//   // Add our marker cluster layer to the map
 


