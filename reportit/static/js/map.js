// ---------------------------------------------

// center, zoom, and maxZoom of the map
var center = [52.45, 13.35],
  zoom = 2,
  moreZoom = 9,
  maxZoom = 18;

// get location using the Geolocation interface
var geoLocationOptions = {
  enableHighAccuracy: true,
  timeout: 10000,
  maximumAge: 0,
};

var myLat, myLng, display_name, myMarker;

function cb(data) {
  display_name = data.display_name;
  myMarker
    .addTo(map)
    .bindPopup(
      `<b>Your location</b><br>
                   Latitude: ${myLat} <br>
                   Longitude: ${myLng} <br> 
                <b>Your address</b><br>
                   ${display_name} <br
                 `
    )
    .openPopup();
  document.getElementById("demo").innerHTML = display_name;
}

function success(position) {
  myLat = position.coords.latitude.toFixed(6);
  myLng = position.coords.longitude.toFixed(6);
  latLng = [myLat, myLng];
  map.setZoom(200);
  map.panTo(latLng);

  cordJson = JSON.stringify({
    type: "Feature",
    properties: {},
    geometry: {
      type: "Point",
      coordinates: [position.coords.longitude, position.coords.latitude],
    },
  });

 

  var script = document.createElement("script");
  script.id = "nominatim";
  script.async = true; // This is required for asynchronous execution
  script.src =
    "https://nominatim.openstreetmap.org/reverse?json_callback=cb&format=json&lat=" +
    myLat +
    "&lon=" +
    myLng +
    "&zoom=27&addressdetails=1";
  document.body.appendChild(script);
  myMarker = L.marker(latLng);
  document.body.removeChild(script);
}

function error(err) {
  console.warn(`ERROR(${err.code}): ${err.message}`);
}

navigator.geolocation.getCurrentPosition(success, error, geoLocationOptions);

// create the map
var map = L.map("map", {
  contextmenu: true,
  contextmenuWidth: 140,
  contextmenuItems: [
    {
      text: "Center map here",
      callback: centerMap,
    },
    {
      text: "Add marker here",
      callback: addMarker,
    },
  ],
}).setView(center, zoom);

// set up the OSM layer
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: maxZoom,
}).addTo(map);

// function to center map
function centerMap(e) {
  map.panTo(e.latlng);
}

// function to add marker
function addMarker(e) {
  L.marker(e.latlng).addTo(map);
}

// -----------------------------------------------------------------


// --------------------------Get Data Json ------------------------------------
function submitForm(event) {
  // Prevent the form from submitting.
  event.preventDefault();
  // Set url for submission and collect data.
  const url = "http://localhost:5000/jsontest";
  const formData = new FormData(event.target);
  // Build the data object.
  const data = { lat: myLat, lng: myLng, DateTime: dateTime ,markerLat: markerLat, markerLng :markerLng };
 
  formData.forEach((value, key) => (data[key] = value));
  // Log the data.
  console.log(JSON.stringify(data));
  console.log(data)

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/jsontest", true);
  xhttp.setRequestHeader("Content-Type", "application/json");
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      // Response
      var response = this.responseText;
      console.log(response);
      // window.location.href = "/submission";
      window.location.href = response;
    }
  };
  xhttp.send(JSON.stringify(data));
}



// --------------------------Preview Image-----------------------------
var loadFile = function(event) {
	var image = document.getElementById('output');
	image.src = URL.createObjectURL(event.target.files[0]);
};


// ------------------------------base46-------------------------------------

var y
function encodeImageFileAsURL(element) {
  var image = document.getElementById('output');
	image.src = URL.createObjectURL(event.target.files[0]);
  var file = element.files[0];
  var reader = new FileReader();
  reader.onloadend = function() {
    console.log(reader.result)
    y = reader.result
  }
  reader.readAsDataURL(file);
}


// --------------------------------date time------------------------------------
var dateTime
//Pad given value to the left with "0"
function AddZero(num) {
  return (num >= 0 && num < 10) ? "0" + num : num + "";
}
window.onload = function() {
  var now = new Date();
  var strDateTime = [[AddZero(now.getDate()), 
      AddZero(now.getMonth() + 1), 
      now.getFullYear()].join("/"), 
      [AddZero(now.getHours()), 
      AddZero(now.getMinutes())].join(":"), 
      now.getHours() >= 12 ? "PM" : "AM"].join(" ");
  dateTime=strDateTime
};
// ----------------------------------------------------------------------------------



// --------------------------------------Marker Manually--------------------------
var marker = null;
var markerLat
var markerLng
map.on('click', function (e) {
    if (marker !== null) {
        map.removeLayer(marker);
    }
    marker = L.marker(e.latlng).addTo(map);
    markerCord=e.latlng
    lat="lat"
    markerLat=markerCord[lat]
    lng="lng"
    markerLng=markerCord[lng]
});