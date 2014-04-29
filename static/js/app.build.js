/*
    Config for build / minification of Javascript files. In general, all dependencies specified in main.js must be added here. Also, any JS files required that are not part of the top 'define' call, must be added to the 'include' files.
*/

({
    baseUrl: ".",
    paths:{
        text:'libs/text',
        domReady:'libs/domReady',
        underscore:'libs/underscore',
        Backbone:'libs/backbone',
        marionette: 'libs/backbone.marionette.min',
        leaflet: 'libs/leaflet/leaflet',
        'leaflet-draw': 'libs/leaflet/leaflet.draw',
        moment: 'libs/moment.min',
        select2: 'libs/select2/select2',
        nouislider: 'libs/nouislider/jquery.nouislider.min',
		backbone_paginator: 'libs/backbone.paginator',
        backbone_nested: 'libs/backbone-nested-v1.1.2.min',
        jquery:'libs/jquery-1.8.3.min'
    },
    shim: {
        leaflet: {
            exports: 'L'
        },
        'leaflet-draw': {
            deps: ['leaflet'],
            exports: 'L'
        },
        Backbone:{
            deps:['underscore', 'jquery'],
            exports:'Backbone'
        },
        moment: {
            exports: 'moment'
        },
		backbone_paginator : {
			deps:['Backbone'],
            exports: 'Backbone'
		},
        backbone_nested: {
            deps:['Backbone'],
            exports: 'Backbone'
        },
        marionette: {
            deps:['Backbone'],
            exports: 'Marionette'
        },
        underscore:{
            exports:'_'
        },
//		cs: {
//			deps:['coffee-script']
//		},
		jquery : {
			exports:'$'
		},
        select2: {
            deps: ['jquery'],
            exports: '$'
        },
        nouislider: {
            deps: ['jquery'],
            exports: '$'
        }
    },

//    paths: {
//        jquery: "some/other/jquery"
//    },
    name: "main",
    out: "build/main.js",
    include: [
        'app/views/pagination',
        'app/views/recentplaces',
        'app/views/placesview',
        'app/views/placedetail',
        'app/views/origins',
        'app/views/relating_from',
        'app/views/feature_codes',
        'app/helpers/modal',
        'app/views/modals/login',
        'app/views/modals/logout',
        'app/views/modals/new_place',
        'app/views/modals/revert_place',
        'app/views/modals/save_place',
        'app/views/modals/relate_places',
        'app/views/modals/delete_relation',
        'app/views/modals/error',
        'app/views/tabs/admin_boundaries',
        'app/views/tabs/altnames',
        'app/views/tabs/relations',
        'app/views/tabs/revisions',
        'app/views/tabs/similar_places',
        'app/views/layouts/results',
        'app/collections/admin_boundaries',
        'app/collections/alternate_names',
        'app/collections/existing_relations',
        'app/collections/search_relations',
        'app/collections/revisions',
        'app/collections/similar_places'
    ]

})
