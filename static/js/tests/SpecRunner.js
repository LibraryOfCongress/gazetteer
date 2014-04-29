require.config({
    baseUrl: "/static/js/",
    urlArgs: 'cb=' + Math.random(),
    paths: {
        text:'libs/text',
        underscore:'libs/underscore',
        // Backbone.js library
        Backbone:'libs/backbone',
        marionette: 'libs/backbone.marionette.min',
        leaflet: 'libs/leaflet/leaflet',
        backbone_paginator: 'libs/backbone.paginator',
        jquery:'libs/jquery-1.8.3.min',
        jasmine: 'libs/jasmine-1.3.1/jasmine',
        'jasmine-html': 'libs/jasmine-1.3.1/jasmine-html',
        'jasmine-require': 'libs/jasmine-1.3.1/jasmine-require',
        spec: 'tests/spec/'
    },
    shim: {
        jquery: {
            exports: '$'
        },
        leaflet: {
            exports: 'L'
        },
        underscore: {
            exports: "_"
        },
        Backbone: {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
	    backbone_paginator : {
		    deps:['Backbone']
	    },
        marionette: {
            deps:['Backbone'],
            exports: 'Marionette'
        },
        jasmine: {
            exports: 'jasmine'
        },
        'jasmine-html': {
            deps: ['jasmine', 'jasmine-require'],
            exports: 'jasmine'
        },

    }
});

require(['underscore', 'jquery', 'jasmine-html'], function(_, $, jasmine){
 
    var jasmineEnv = jasmine.getEnv();
    jasmineEnv.updateInterval = 1000;

    var htmlReporter = new jasmine.HtmlReporter();

    jasmineEnv.addReporter(htmlReporter);

    jasmineEnv.specFilter = function(spec) {
        return htmlReporter.specFilter(spec);
    };

    var specs = [];
    specs.push('spec/collections/PlacesSpec')


    $(function(){
        require(specs, function(){
            jasmineEnv.execute();
        });
    });
 
});

