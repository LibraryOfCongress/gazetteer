'use strict';

(function() {

    window.$G = {

        //Leaflet Style Definitions
        styles: {
            geojsonDefaultCSS: {
                    radius: 7,
                    fillColor: "#7CA0C7",
                    color: "#18385A",
                    weight: 1,
                    opacity: 1,
                    fillOpacity: 0.6
            },
            geojsonHighlightedCSS: {
                radius: 7,
                fillColor: '#F15913',
                color: '#f00',
                weight: 1,
                opacity: 1,
                fillOpacity: 1
            },
            similarPlacesDefaultCSS: {
                radius: 6,
                fillColor: 'green',
                color: 'green',
                weight: 1,
                opacity: 0.8,
                fillOpacity: 0.5
            },
            similarPlacesHighlightedCSS: {
                radius: 8,
                opacity: 1,
                weight: 1,
                fillOpacity: 1,
                color: '#000'
            }
        },

        //Common map definitions
        //TODO: make osmUrl configurable in settings.py
        //osmUrl: 'http://a.tiles.mapbox.com/v3/mattknutzen.map-cja7umx7/{z}/{x}/{y}.png',
        osmUrl: 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        osmAttrib: 'Map data © openstreetmap contributors',

        //api variables
        apiBase: '/1.0/place/',
        placeUrlPrefix: "/feature/"
    }

})();

//pass in the properties and get the admin boundary string
function toAdminString(props){
        var admin_names = ""
        if (props.admin.length > 0){
        var name_array = ["","","","","", ""] //ADM0, ADM1, ADM2, ADM3, ADM4, others
        $.each(props.admin, function(i, admin) {
            if (admin.feature_code == "ADM0") {
                name_array[0] = name_array[0] + " " + admin.name
            }else if (admin.feature_code == "ADM1"){
                name_array[1] = name_array[1] + " " + admin.name
            }else if (admin.feature_code == "ADM2"){
                name_array[2] = name_array[2] + " " + admin.name
            }else if (admin.feature_code == "ADM3"){
                name_array[3] = name_array[3] + " " + admin.name
            }else if (admin.feature_code == "ADM4"){
                name_array[4] = name_array[4] + " " + admin.name
            }else {
                name_array[5] = name_array[5] + " " + admin.name
            }

        });
        var name_array_clean = []
        $.each(name_array, function(i, name){
            if (name != ""){
                name_array_clean.push(name)
                }
        });

        $.each(name_array_clean.reverse(), function(i, name){
            var comma = ","
            if (i == 0) comma = ""
            admin_names = admin_names + comma + name
        }); 
    }
    return admin_names
    }

