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
var map = L.map("mapm", {
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
  const data = { lat: myLat, lng: myLng };
 
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
  // xhttp.send(JSON.stringify(data));
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

// ----------------------------------------------------------------------------------



// <!-- --------------------------------Doamin/Subtype----------------------------------------------- -->
              
var Utility = ["Water","Gas","Sewage","Electric","Telecommunication"];
var Poullution = ["Noise Pollution","Air Pollution","Industrial Pollution","Soil Pollution","Water Pollution"];
var Road = ["Accidents","Lamps","Hales","Barriers"];
var Disasters = ["Earthquakes","Flloods","Landslides","Torrnados"];

// --------------------------Sub subUtility-----------------------------
    var Water= ["Leakage","Quality","Cut","Explosion","Stealing","Overflow","Failure"];
    var Sewage = ["Leakage","Quality","Cut","Explosion","Stealing","Overflow","Failure"]; 
    var Gas =  ["Leakage","Quality","Cut","Explosion","Stealing","Failure"];
    var Electric= ["Quality","Cut","Explosion","Stealing","Failure"]; 
    var Telecom = ["Cut","Stealing","Failure"]
// ---------------------------------------------------------------------

function updateTwo() {
    var  problem = document.getElementById("1");
    var subProblem = document.getElementById("2");
    var selected = problem.options[problem.selectedIndex].value;
    // var SubUtility = document.getElementById("3");
    var i;
    for(i = subProblem.options.length - 1 ; i >= 0 ; i--) {
        subProblem.remove(i);
        // SubUtility.remove(i);
    }
    if(selected=="Water"){
        for(var i = 0; i < Water.length; i++) {
            addOption(subProblem,Water[i]);
        }
        
    } else if(selected=="Sewage"){
      for(var i = 0; i < Sewage.length; i++) {
          addOption(subProblem,Sewage[i]);
        } 
      
    } else if(selected=="Gas"){
      for(var i = 0; i < Gas.length; i++) {
          addOption(subProblem,Gas[i]);
        } 
      
    } else if(selected=="Electric"){
      for(var i = 0; i < Electric.length; i++) {
          addOption(subProblem,Electric[i]);
        } 
      
    } else if(selected=="Telecom"){
      for(var i = 0; i < Telecom.length; i++) {
          addOption(subProblem,Telecom[i]);
        } 
      
    } 
    else if(selected=="Poullution") {
        for(var j = 0; j < Poullution.length; j++) {
            addOption(subProblem,Poullution[j]);
        }
    } else if(selected=="Road") {
        for(var k = 0; k < Road.length; k++) {
            addOption(subProblem,Road[k]);
        }

    } else if(selected=="Disasters") {
        for(var m = 0; m < Disasters.length; m++) {
            addOption(subProblem,Disasters[m]);
        }
    }


    
}

addOption = function(option, value) {
    var opt = document.createElement('option');
    opt.innerHTML = value;
    opt.value = value;
    option.appendChild(opt);
    
}

// <!-- -------------------------------------------------------------------------------------------------- -->
window.onload = function() {
  updateTwo()
  };
