define(['jquery', 'app/core/mediator', 'app/collections/places', 'app/models/place', 'require'], function($, mediator, Places, Place, require) { 
    return {
        //Home route, do nothing.
        "home": function() {
        },

        //Search route
        "search": function() {
            var app = require("app/app");
            var queryString = window.location.search;
            var searchHelper = require("app/helpers/search");
            //get query-string from URL, convert to JSON and set server_api settings for Places collection with search params
            var queryJSON = searchHelper.queryStringToJSON(queryString);
            var places = app.collections.places = new Places().setServerApi(queryJSON);
            //Call mediator to update search UI based on query params
            mediator.commands.execute("search:updateUI", queryJSON);
            //Call mediator to fetch results
            mediator.commands.execute("fetchPlaces", places);
        },

        //Place detail route, called with place id, and optionally 'tab' to show
        "detail": function(id, tab) {
            if (typeof(tab) == 'undefined') {
                tab = false;
            }
            var app = require("app/app");
            //call mediator to load place and execute openPlace on loaded place
            mediator.commands.execute("getPlaceAsync", id, function(place) {
                mediator.commands.execute("openPlace", place, tab);
            });
        }
    }   

});
