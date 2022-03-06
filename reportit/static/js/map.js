let map = L.map('map',{
    center: [30.5, 30.9],
    zoom: 20}
);

var myBaseMap =L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);
myBaseMap.addTo(map)



//------------------------------------------------------------

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

//         const request = new XMLHttpRequest()
//         request.open('POST','/jsontest')
//         request.send()
   
//         // var map = new google.maps.Map(document.getElementById("dvMap"));
//     });
// } 

  

map.locate({setView: true, maxZoom: 100});



function onLocationFound(e) {
    
    var radius = e.accuracy / 2;
    L.marker(e.latlng).addTo(map)
      .bindPopup("Your Location").openPopup();
    L.circle(e.latlng, radius).addTo(map);
  }
  
  map.on('locationfound', onLocationFound);
  map.locate({setView: true,  maxZoom: 100});



// -------------------------------------------

  
function geoFindMe() {

  const status = document.querySelector('#status');
  const mapLink = document.querySelector('#map-link');

  mapLink.href = '';
  mapLink.textContent = '';

  function success(position) {
    const latitude  = position.coords.latitude;
    const longitude = position.coords.longitude;

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

    status.textContent = '';
    mapLink.href = `https://www.openstreetmap.org/#map=18/${latitude}/${longitude}`;
    mapLink.textContent = `Latitude: ${latitude} °, Longitude: ${longitude} °`;
  }

  function error() {
    status.textContent = 'Unable to retrieve your location';
  }

  if(!navigator.geolocation) {
    status.textContent = 'Geolocation is not supported by your browser';
  } else {
    status.textContent = 'Locating…';
    navigator.geolocation.getCurrentPosition(success, error);
  }

  

}

document.querySelector('#find-me').addEventListener('click', geoFindMe);




//-------------------------------------------


