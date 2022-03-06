// let map = L.map('map',{
//     center: [30.5, 30.9],
//     zoom: 20}
// );

// var myBaseMap =L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
//   }).addTo(map);
// myBaseMap.addTo(map)

// ------------------------------------------------------------------------

// map.on("click", function (event) {
//     console.log(  event.latlng.toString());
//     L.marker(event.latlng).addTo(map)
//     alert('Your Cordinates is: '  + event.latlng.toString());
    

     
//      y={
//         "type": "Feature",
//         "properties": {},
//         "geometry": {
//           "type": "Point",
//           "coordinates": [
//             event.latlng.toString()
//           ]
//         }
//       }


//      console.log({
//         "type": "Feature",
//         "properties": {},
//         "geometry": {
//           "type": "Point",
//           "coordinates": [
//             event.latlng.toString()
//           ]
//         }
//       })
//   });



// -----------------Lat/long GeoJson-------------------------


// if (navigator.geolocation) {
//     navigator.geolocation.getCurrentPosition(function (p) {
//         var LatLng = new google.maps.LatLng(p.coords.latitude, p.coords.longitude);

    
        
//         cordJson=(JSON.stringify({
//             "type": "Feature",
//             "properties": {},
//             "geometry": {
//               "type": "Point",
//               "coordinates": [
//                 p.coords.latitude, p.coords.longitude
//               ]
//             }
//           }))

//         console.log(cordJson)

        // const request = new XMLHttpRequest()
        // request.open('POST','/jsontest')
        // request.send()
   
//         // var map = new google.maps.Map(document.getElementById("dvMap"));
//     });
// } 

// ---------------------------------------------

// center, zoom, and maxZoom of the map
var center = [52.45, 13.35],
  zoom = 2,
  moreZoom = 9,
  maxZoom = 18

// get location using the Geolocation interface
var geoLocationOptions = {
  enableHighAccuracy: true,
  timeout: 10000,
  maximumAge: 0
}

var myLat, myLng, display_name, myMarker

function cb(data) {
  display_name = data.display_name
  myMarker.addTo(map)
    .bindPopup(`<b>Your location</b><br>
                   Latitude: ${myLat} <br>
                   Longitude: ${myLng} <br> 
                <b>Your address</b><br>
                   ${display_name} <br
                 `).openPopup()
                 document.getElementById("demo").innerHTML = display_name;
}

function success(position) {

  myLat = position.coords.latitude.toFixed(6)
  myLng = position.coords.longitude.toFixed(6)
  latLng = [myLat, myLng]
  map.setZoom(200)
  map.panTo(latLng)

  cordJson=(JSON.stringify({
    "type": "Feature",
    "properties": {},
    "geometry": {
      "type": "Point",
      "coordinates": [
        position.coords.latitude, position.coords.longitude
      ]
    }
  }))

console.log(cordJson)

  var script = document.createElement('script')
  script.id = 'nominatim'
  script.async = true // This is required for asynchronous execution
  script.src = 'https://nominatim.openstreetmap.org/reverse?json_callback=cb&format=json&lat=' + myLat + '&lon=' +
    myLng + '&zoom=27&addressdetails=1'
  document.body.appendChild(script)
  myMarker = L.marker(latLng)
  document.body.removeChild(script)
}

function error(err) {
  console.warn(`ERROR(${err.code}): ${err.message}`)
}

navigator.geolocation.getCurrentPosition(success, error, geoLocationOptions)



// create the map
var map = L.map('map', {
  contextmenu: true,
  contextmenuWidth: 140,
  contextmenuItems: [{
      text: 'Center map here',
      callback: centerMap
    },
    {
      text: 'Add marker here',
      callback: addMarker
    }
  ]
}).setView(center, zoom)



// set up the OSM layer
L.tileLayer(
  'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: maxZoom
  }).addTo(map)


// function to center map
function centerMap(e) {
  map.panTo(e.latlng)
}

// function to add marker
function addMarker(e) {
  L.marker(e.latlng).addTo(map)
}



// ------------------------------------------------------------------------------- 

// map.locate({setView: true, maxZoom: 100});

// function onLocationFound(e) {
    
//     var radius = e.accuracy / 2;
//     L.marker(e.latlng).addTo(map)
//       .bindPopup("Your Location").openPopup();
//     L.circle(e.latlng, radius).addTo(map);
//   }
  
//   map.on('locationfound', onLocationFound);
//   map.locate({setView: true,  maxZoom: 100});

//------------------------------------------------------------------



// -----------------------------------------------------------------

function submitForm(event) {
  // Prevent the form from submitting.
  event.preventDefault();
  // Set url for submission and collect data.
  const url = "https://example.com/...";
  const formData = new FormData(event.target);
  // Build the data object.
  const data = {};
  formData.forEach((value, key) => (data[key] = value));
  // Log the data.
  console.log(data);
 
}
// ------------------------------------------------------------

// window.onload = function() {
//   geoFindMe();
// };

// -----------------------------------------------------------



