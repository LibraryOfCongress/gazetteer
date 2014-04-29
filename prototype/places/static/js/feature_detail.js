
var map;

$(function() {
   
    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib='Map data © openstreetmap contributors';
    var osm = new L.TileLayer(osmUrl,{minZoom:1,maxZoom:18,attribution:osmAttrib});
//    var center = L.GeoJSON.coordsToLatLng(FEATURE_GEOJSON.geometry.coordinates);
    map = new L.Map('map', {layers: [osm], center: [0,0], zoom: 8 });
    featureLayer = L.geoJson(FEATURE_GEOJSON, {

    }).addTo(map);
    var bounds = featureLayer.getBounds();
    map.fitBounds(bounds);
    
});
