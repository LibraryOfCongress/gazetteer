/*
    Sets up RequireJS config, loads dependencies, and starts the app.
    Any dependencies added here must also be added to app.build.js for the build / minification.
*/

require.config({
    urlArgs: 'cb=' + Math.random(),
    waitSeconds: 45,
    paths:{
        // RequireJS plugin
        text:'libs/text',
        // RequireJS plugin
        domReady:'libs/domReady',
        // underscore library
        underscore:'libs/underscore',
        // Backbone.js library
        Backbone:'libs/backbone',
        //backbone marionette 1.0.0rc6
        marionette: 'libs/backbone.marionette.min',
        // leaflet.js
        leaflet: 'libs/leaflet/leaflet',

        'leaflet-draw': 'libs/leaflet/leaflet.draw',
        //http://momentjs.com/ for formatting dates
        moment: 'libs/moment.min',
        //Select2 for autocompletes: https://github.com/ivaynberg/select2
        select2: 'libs/select2/select2',

        //for time sliders - http://refreshless.com/nouislider/
        nouislider: 'libs/nouislider/jquery.nouislider.min',

		backbone_paginator: 'libs/backbone.paginator',

        //deal with nested properties in model: https://github.com/afeld/backbone-nested/
        backbone_nested: 'libs/backbone-nested-v1.1.2.min',
        // jQuery
        jquery:'libs/jquery-1.8.3.min'
    },
    shim:{
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
    }
});

require(["app/app", "domReady"],function(app, domReady){
    domReady(function() {
        app.start();
        window.$G = app; //global that's accessible from outside makes it easier to debug. Can be removed, NOT to be used in app code.
    });
});
