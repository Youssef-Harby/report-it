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


if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (p) {
        var LatLng = new google.maps.LatLng(p.coords.latitude, p.coords.longitude);

    
        
        cordJson=(JSON.stringify({
            "type": "Feature",
            "properties": {},
            "geometry": {
              "type": "Point",
              "coordinates": [
                p.coords.latitude, p.coords.longitude
              ]
            }
          }))

        console.log(cordJson)

        const request = new XMLHttpRequest()
        request.open('POST','/jsontest')
        request.send()
   
        // var map = new google.maps.Map(document.getElementById("dvMap"));
    });
} 

  

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

  
   




//-------------------------------------------


