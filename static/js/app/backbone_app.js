/*
    # Models #
*/

/*
    main model for a 'place', would be instantiated with: new Place(placeGeoJSON); 
    QUESTION: do we need separate models for a place 'result' and place 'detail'?
    QUESTION: do we use the GeoJSON as is, or do we 'flatten' properties and Feature?
*/ 
var PlaceModel = Backbone.Model.extend({

});


/*
    model for search queries - contains search parameters as properties, and is responsible for refreshing views associated with it on 'change'
    QUESTION: should 'search' be a model at all? what's the best way to handle storing / validation of search params, as well as ensuring views / models are refreshed on change?
*/
var SearchModel = Backbone.Model.extend({
    
});


//model to hold revisions for a place, needs to have a "foreign key" to Place
var RevisionModel = Backbone.Model.extend({

});


//holds all relations for a place
var RelationsModel = Backbone.Model.extend({

});


/*
    # Collections #
*/

/*
    Is a collection of "Places", is linked to a SearchModel and refreshes whenever SearchModel changes
    TODO: use Backbone.Paginator.requestPager from https://github.com/addyosmani/backbone.paginator
*/
var ResultList = Backbone.Collection.extend({

});


//holds a list of revisions for a place
var RevisionsList = Backbone.Collection.extend({


});

//holds a list of relations for a place
var RelationsList = Backbone.Collection.extend({


});



/*
    # Views #
*/


/*
    view to handle all interfacing with the map, shall subscribe to events in the UI to zoom into places, highlight places, etc. and also publish events like "moved" for other views to subscribe to.
*/
var MapView = Backbone.View.extend({

});


/*
    view for search and filter UI    
*/
var SearchView = Backbone.View.extend({

});


/*
    view to display results in main results section - this view will handle updating of pagination properties, etc. and instantiating and rendering result items. 
    There will also be views to display results like 'similar places' on the place detail view, hence this is 'main'. 
    QUESTION: do we need a BaseResultsView which various ResultsViews can inherit from?
    
*/
var MainResultsView = Backbone.View.extend({

});


/*
    view for each item in the main results view
*/
var MainResultItemView = Backbone.View.extend({

});
 

/*
    main view for place detail
*/
var PlaceDetailView = Backbone.View.extend({

});


// view for place revisions
var PlaceRevisionsView = Backbone.View.extend({

});


// view for revisions item
var PlaceRevisionItemView = Backbone.View.extend({

});


// view for place relations
var PlaceRelationsView = Backbone.View.extend({

});


// view for place relation item
var PlaceRelationItemView = Backbone.View.extend({

});


/*
    view to show 'similar places' on place detail page as well as searching for arbitrary places to make relationships to
    QUESTION: can this use the same SearchModel and ResultList definition to manage itself?    
*/
var SimilarResultsView = Backbone.View.extend({
    
});


//handles rendering a single similar place item - will be responsible for showing conflation UI, adding to 'relations', etc.
var SimilarResultItemView = Backbone.View.extend({

});





/*
    # Router definition #
*/
var Router = Backbone.Router.extend({

    routes: {
        '': 'search',
        'place/:id': 'detail
    },

    'search': function() {

    },

    'detail': function(id) {

    }

});



/*
    Library to handle API calls - defines $G.api.
    This library should not depend on Backbone / be usable in other JS contexts and should provide a JS wrapper over the back-end API. Each method should correspond to an API call and return a jQuery xHR object. A custom Backbone.sync function will use this API object to make api calls.      
*/
(function($) {
    var API = function() {

        function callAPI(url, method, data) {
            return $.ajax({
                'url': $G.apiBase + url,
                'data': data,
                'type': method,
                'dataType': 'json'        
            });            
        }

        function getPlaceURL(geojson) {
            return geojson.properties.id + ".json";
        }

        /*
            'save_place' method
        */
        this.save_place = function(geojson, comment) {
            var url = getPlaceURL(geojson);
            geojson.comment = comment;
            var data = JSON.stringify(geojson);
            return callAPI(url, 'PUT', data);                        
        }

  
    };

    $G.api = new API();

})(jQuery);
