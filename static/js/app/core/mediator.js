define(['Backbone', 'marionette', 'underscore', 'require', 'app/settings'], function(Backbone, Marionette, _, require, settings) {

    //Setup event aggregator, command executor, and request / response objects
    var events = new Backbone.Wreqr.EventAggregator(),
        commands = new Backbone.Wreqr.Commands(),
        requests = new Backbone.Wreqr.RequestResponse();


    /*
        If we are in debug mode, log all events on the mediator to console
    */
    if (settings.debug) {
        events.on("all", function(eventType) {
            console.log("event fired: ", eventType);
        });
    }
   
    /*
        Triggered when user logs in through login modal. Is listened to by views that need to display differently for logged in users
    */ 
    events.on("login", function(user) {
        var app = require('app/app');
        app.user = user;
    });

    /*
        Similar, for logout.
    */
    events.on("logout", function() {
        var app = require('app/app');
        app.user = {};
    });

    /*
        get place object by id, when we are sure the place exists, either as the current place detail view or in the results collection, returns place immediately. Used by the getPopupHTML() handler in the map view. 
    */
    requests.addHandler("getPlace", function(id) {
        var app = require('app/app');
        if (app.collections.places && app.collections.places.get(id)) {
            return app.collections.places.get(id);
        }
        if (app.placeDetail.currentView && app.placeDetail.currentView.model.id === id) {
            return app.placeDetail.currentView.model;
        }
        return false;   
    });



    /*
        Used when we are not sure if the place exists on the front-end. Takes place id and callback to call with success -- if place id found, calls callback immediately, else, uses API to fetch place and then calls call-back. Is used by the router / controller when navigating to place detail page.
    */
    commands.addHandler("getPlaceAsync", function(id, callback) {
        var place = requests.request("getPlace", id);
        if (place) {
            callback(place);
        } else {
            require(['app/models/place', 'app/settings'], function(Place, settings) {
                var url = settings.api_base + "place/" + id + ".json";
                $.getJSON(url, {}, function(geojson) { //FIXME: should be ajax utils or so
                    var place = new Place(geojson);
                    callback(place);
                });
            });
        }
    });


    /*
        FIXME: this should be removed in favour of "getCurrentView"
    */
    requests.addHandler("isResultsView", function() {
        var app = require('app/app');
        return app.results.$el && app.results.$el.is(":visible");
    });

    /*
        Gets the current 'open tab' name - either results, place or selected.
    */
    requests.addHandler("getCurrentView", function() {
        var app = require('app/app');
        return app.views.navigation.getOpenTabName();
    });


    /*
        Returns true / false based on if "search in BBox" is active.
    */
    requests.addHandler("isBBoxSearch", function() {
        var app = require('app/app');
        return app.views.search.ui.searchInBBox.is(":checked");
    });


    /*
        Returns current place displayed in the place detail view, false if no place is loaded.
    */
    requests.addHandler("getCurrentPlace", function() {
        var app = require('app/app');
        if (app.placeDetail.currentView) {
            return app.placeDetail.currentView.model;
        } else {
            return false;
        }
    });


    /*
        Returns true / false based on whether place is part of selectedPlaces collection
    */
    requests.addHandler("place:isSelected", function(place) {
        var app = require('app/app');
        if (app.collections.selectedPlaces.contains(place)) { //FIXME: do we need both calls to check for object and by id? Just by id should work?
            return true;
        }
        if (app.collections.selectedPlaces.get(place.id)) {
            return true;
        }
        return false;
    });


    /*
        Gets current user object, or false is user is not logged in.
    */
    requests.addHandler("getUser", function() {
        var app = require('app/app');
        if (!_.isEmpty(app.user)) {
            return app.user;
        } else {
            return false;
        }
    });


    /*
        Update Search UI when navigating from a URL
    */
    commands.addHandler("search:updateUI", function(queryObj) {
        var app = require('app/app');
        app.views.search.setSearchParams(queryObj);
        if (queryObj.bbox) {
            app.views.map.setBBox(queryObj.bbox);
        }
        if (queryObj.origins) {
            app.collections.origins.markFromQuery(queryObj.origins);
        }
        if (queryObj.feature_codes) {
            app.collections.featureCodes.markFromQuery(queryObj.feature_codes);
        }
    });

    /*
        Submit a new search, gets search URL from Search Helper, and navigates to it, triggering the route.
    */
    commands.addHandler("search:submit", function() {
        require(['app/app', 'app/core/controller'], function(app, controller) {
            var app = require('app/app');
            //app.views.header.hideSearch();
            app.router.navigate(app.helpers.search.getSearchURL(), {'trigger': true});
            controller.search();
        });
    });

    /*
        Set page number when navigating to a new page from the pagination view (or set to '1' when making a fresh search
    */
    commands.addHandler("search:setPage", function(page) {
        var app = require('app/app');
        app.views.map.userMovedMap = true;
        app.views.search.setPage(page);
    });


    /*
        Set search to be within bbox, is called by the map view when user action moves the map
    */
    commands.addHandler("search:setWithinBBox", function() {
        var app = require('app/app');
        app.views.search.setWithinBBox();
    });

    /*
        Called just before making AJAX call to fetch place results
    */
    commands.addHandler("search:doLoading", function() {
        var app = require('app/app');
        app.views.search.doLoading();
    });

    /*
        Called after place results have been fetched
    */
    commands.addHandler("search:stopLoading", function() {
        var app = require('app/app');
        app.views.search.stopLoading();
    });

    /*
        Add feature code to feature code filters collection (called when user adds feature code from autocomplete
    */
    commands.addHandler("search:addFeatureCode", function(featureCode) {
        var app = require('app/app');
        app.collections.featureCodes.add(featureCode);
        app.collections.featureCodes.get(featureCode.typ).set("checked", true);
    });

    /*
        Used to highlight a place object on the map, for eg when mousing over a place result
    */
    commands.addHandler("map:highlight", function(place, mapLayer) {
        var app = require('app/app');
        app.views.map.highlight(place, mapLayer);   
    });


    /*
        Unhighlight place, eg. when mouse-out
    */
    commands.addHandler("map:unhighlight", function(place, mapLayer) {
        var app = require('app/app');
        app.views.map.unhighlight(place, mapLayer);
    });


    /*
        Zoom to a place on the map
    */
    commands.addHandler("map:zoomTo", function(place) {
        var app = require('app/app');
        app.views.map.zoomTo(place);

    });

    /*
        Zoom to the extents of a layer on the map, eg. 'results'
    */
    commands.addHandler("map:zoomToLayer", function(layerName) {
        var app = require('app/app');
        var layer = app.views.map[layerName];
        app.views.map.zoomToExtent(layer);
    });


    /*
        Load search results GeoJSON on map, called when places collection fetches result, before parsing
    */
    commands.addHandler("map:loadSearchResults", function(geojson) {
        var app = require('app/app');
        app.views.map.loadSearchResults(geojson);

    });

    /*
        Hide other layers and show current results layer on the map - called when switching "tabs" to Results tab.
    */
    commands.addHandler("map:showResults", function() {
        var app = require('app/app');
        app.views.map.showResults();

    });

    /*
        Load place relations on the map
    */
    commands.addHandler("map:loadRelations", function(relations) {
        var app = require('app/app');
        app.views.map.loadRelations(relations);
    });

    /*
        Remove place relations from map
    */
    commands.addHandler("map:removeRelations", function() {
        var app = require('app/app');
        app.views.map.removeRelations();
    });

    commands.addHandler("map:loadSimilar", function(similarPlaces) {
        var app = require('app/app');
        app.views.map.loadSimilar(similarPlaces);
    });

    commands.addHandler("map:removeSimilar", function() {
        var app = require('app/app');
        app.views.map.removeSimilar();
    });

    /*
        Calls navigation view to show tab heading - for eg. when first time loading results, or place
    */
    commands.addHandler("nav:showTab", function(name) {
        var app = require('app/app');
        app.views.navigation.showTab(name);   
    });

    /*
        Hide tab, FIXME: this was used to hide selected places if all places unselected. Remove if no longer needed.
    */
    commands.addHandler("nav:hideTab", function(name) {
        var app = require('app/app');
        app.views.navigation.hideTab(name);
    });


    /*
        Call this to show a modal view, with modal name and options to pass to modal view. Calls modalHelper to trigger view.
    */
    commands.addHandler("showModal", function(type, options) {
        require(['app/helpers/modal'], function(modalHelper) {
            modalHelper.showModal(type, options);
        });
    });

    /*
        Close currently open modal view
    */
    commands.addHandler("closeModal", function() {
        require(['app/helpers/modal'], function(modalHelper) {
            modalHelper.closeModal();
        });
    });


    /*
        Select place, add to selectedPlaces collection. If place is currently in detail view, set selected toggle to update view.
    */
    commands.addHandler("selectPlace", function(place) {
        var app = require('app/app');
        app.collections.selectedPlaces.add(place);
        app.views.map.addSelectedPlace(place);
        var currentPlace = requests.request("getCurrentPlace");
        if (currentPlace && currentPlace.id === place.id) {
            app.placeDetail.currentView.placeSelected(); 
        }
        place.trigger('select');
    });

    /*
        Unselect place.
    */
    commands.addHandler("unselectPlace", function(place) {
        var app = require('app/app');
        app.collections.selectedPlaces.removePlace(place);
        if (app.collections.places) {
            app.collections.places.unselectPlace(place);
        }
        app.views.map.removeSelectedPlace(place);
        var currentPlace = requests.request("getCurrentPlace");
        if (currentPlace && currentPlace.id === place.id) {
            app.placeDetail.currentView.placeUnselected();
        }
    });

    /*
        Responsible for displaying place detail view and rendering / zooming into on map, optionally passed a tab name to display
        Defaults to displaying alternate names if no tab name is passed.
    */
    commands.addHandler("openPlace", function(place, tab) {
        require(['app/app', 'app/views/placedetail'], function(app, PlaceDetailView) {
            //app.collections.recentPlaces.add(place);
            app.router.navigate(place.get("permalink"));
            var view = new PlaceDetailView({'model': place});
            app.placeDetail.show(view);
            if (!app.placeDetail.$el.is(":visible")) {
                $('.activeContent').removeClass('activeContent').hide();
                app.placeDetail.$el.addClass('activeContent').show();
            } 
            events.trigger("selectTab", "place");
            app.views.map.loadPlace(place);
            place.updateGeometry(); //gets the full resolution geometry and updates map
            if (!tab) {
                tab = 'alternateNames';
            }
            view.showTab(tab);
        });
    });

    /*
        Updates place geometry on the map if we have a higher resolution than the geometry in the results geojson due to simplification
    */
    commands.addHandler("updatePlaceGeometry", function(place) {
        var app = require('app/app');
        app.views.map.placeLayer.clearLayers();
        app.views.map.placeLayer.addData(place);
    });

    /*
        Fetches new Places collection from back-end as search results, displays results.
    */
    commands.addHandler("fetchPlaces", function(places) {
        require(['app/app', 'app/views/layouts/results'], function(app, ResultsLayout) {
            if (app.ui_state.resultsXHR && app.ui_state.resultsXHR.readyState < 4) {
                app.ui_state.resultsXHR.abort();
            }
            commands.execute("search:doLoading");
            app.ui_state.resultsXHR = places.fetch({
                success: function() {
                    commands.execute("search:stopLoading");
                    var resultsLayout = new ResultsLayout({'collection': places});
                    app.results.show(resultsLayout);
                    if (!app.results.$el.is(":visible")) {
                        $('.activeContent').removeClass('activeContent').hide();
                        app.results.$el.addClass('activeContent').show();
                        events.trigger("selectTab", "results");
                    }
                }
            });
        });
    });

    return {
        'events': events,
        'commands': commands,
        'requests': requests
    };

}); 
