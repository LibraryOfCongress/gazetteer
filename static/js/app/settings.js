/*
    Holds app settings, is extended by settings sent by the back-end.
    When app is loaded, settings are loaded from back-end with instance specific settings defined in instance_settings.py and returned by helpers.py get_settings
*/

define([], function() {
    return {
        origins: [],
        featureCodes: [],
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
                weight: 5,
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
        relationChoices: {
            'conflates'     : 'Conflates',
            'contains'      : 'Contains',
            'replaces'      : 'Replaces',
            'subsumes'      : 'Subsumes',
            'comprises'     : 'Comprises',
            'conflated_by'  : 'Is Conflated By',
            'contained_by'  : 'Is Contained By',
            'replaced_by'   : 'Is Replaced By',
            'subsumed_by'   : 'Is Subsumed By',
            'comprised_by'  : 'Is Comprised By'
        }        

    };


});
