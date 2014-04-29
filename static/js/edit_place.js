'use strict';

var map, jsonLayer;

var API_URL = $G.apiBase + place_geojson.properties.id + ".json";
//var API_URL = "/1.0/place/" + place_geojson.properties.id + ".json";

$(function() {
    
//    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
//    var osmAttrib='Map data © openstreetmap contributors';
    var osm = new L.TileLayer($G.osmUrl,{minZoom:1,maxZoom:18,attribution:$G.osmAttrib});
    map = new L.Map('map', {layers: [osm], center: new L.LatLng(34.11577, -93.855211), zoom: 4 });
    
    
    jsonLayer = L.geoJson(place_geojson, {
 
        pointToLayer: function(feature, latlng) {
            return L.circleMarker(latlng, $G.styles.geojsonDefaultCSS);
        }

    }).addTo(map);

    jsonLayer.addData(place_geojson);

    var featureCodeValue = $('#featureCode').val();   
    $('#featureCode').select2({
        ajax: {
            'url': $G.apiBase + "feature_codes.json",
            dataType: 'json',
            quietMillis: 100,
            data: function(term, page) {
                return {
                    q: term,
                    page_limit: 10,
                    page: page
                }
            },
            results: function(data, page) {
                var more = data.has_next;
                return {results: data.items, more: more};
            }
        },
        formatResult: function(item) {
            return "<div>" + item.cls + ":" + item.typ + " " + item.name + "<div style='font-size:12px'><i>" + item.description + "</i></div></div>"
        },
        formatSelection: function(item) {
            return item.typ;           
            //return "<div data-id='" + item.id + "'>" + item.first_name + " " + item.last_name + "</div>";
        },
        initSelection: function(elem, callback) {
            var val = $(elem).val();
            var data = {
                'id': featureCodeValue,
                'typ': featureCodeValue
            };
            callback(data); 
        }
    });
    

    $('#placeForm').submit(function(e) {
        e.preventDefault();
        var data = {
            'name': $('#placeName').val(),
            'feature_code': $('#featureCode').val()
        };
        $.extend(place_geojson.properties, data);
        $('#saveNotification').text("Saving...");
        var json = JSON.stringify(place_geojson);
        var $xhr = $.ajax({
            'url': API_URL,
            'data': json,
            'type': 'PUT',
            'dataType': 'json'
        })
        .success(function(response) {
                $('#saveNotification').text("Saved");
                //console.log(response);
        })
        .fail(function(response) {
            alert("error saving");
            $('#saveNotification').text(response.error);
        });     
    });  
});
