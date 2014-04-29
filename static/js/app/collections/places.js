define(['Backbone','app/models/place', 'app/settings', 'app/core/mediator', 'app/helpers/search', 'backbone_paginator'], function(Backbone, Place, settings, mediator, searchHelper) {

    var Places = Backbone.Paginator.requestPager.extend({
        'model': Place,
        'paginator_core': {
            'type': 'GET',
            'url': function() {
                return settings.api_base + 'place/search.json?';
            },
            'dataType': 'json'
        },
        'paginator_ui': {
            'firstPage': 1,
            'currentPage': 1,
            'perPage': 50
        },
        'server_api': {
        },

        //since our server-side API URL and client-side urls are different, we store the values we need for the client-side url in 'client_api'
        //FIXME: name 'client_api' something better?
        'client_api': {
            'q': '',
            'origins': '',
            'feature_codes': ''
        },

        //is called from the controller with the URL options
        //FIXME: since we are setting client URL and server URL values, maybe rename to 'setApi' or 'setAPI' ?
        'setServerApi': function(options) {
            this.server_api.simplify = true;
            this.server_api.q = this.client_api.q = options.q || '';
            this.client_api.origins = options.origins ? options.origins : '';
            this.client_api.feature_codes = options.feature_codes ? options.feature_codes : '';
            this.server_api.q = options.origins ? this.server_api.q + " " + searchHelper.getOriginQuery(options.origins) : this.server_api.q;
            this.server_api.q = options.feature_codes ? this.server_api.q + " " + searchHelper.getFeatureCodeQuery(options.feature_codes) : this.server_api.q;
            this.server_api.bbox = options.bbox || null;
            this.server_api.start_date = options.start_date || null;
            this.server_api.end_date = options.end_date || null;
            this.server_api.feature_type = options.feature_type || null;
            this.server_api.page = options.page || null;
            return this;    
        },
       
        'getSearchURL': function() {
            var queryObj = this.getQueryObj();
            queryObj.q = this.client_api.q;
            delete(queryObj.simplify);
            if (this.client_api.origins) {
                queryObj.origins = this.client_api.origins;
            } else {
                delete(queryObj.origins);
            }
            if (this.client_api.feature_codes) {
                queryObj.feature_codes = this.client_api.feature_codes;
            } else {
                delete(queryObj.feature_codes);
            }
            return settings.app_base + 'search' + searchHelper.JSONToQueryString(queryObj);
        },

        'getQueryObj': function() {
            var that = this;
            var queryAttributes = {};
            _.each(_.result(that, "server_api"), function(value, key){
                if( _.isFunction(value) ) {
                    value = _.bind(value, that);
                    value = value();
                }
                if (value) {
                    queryAttributes[key] = value;
                }
            });
            return queryAttributes;
        },
 
        'getQueryString': function() {
            return searchHelper.JSONToQueryString(this.getQueryObj());
        },
        'getGeojsonURL': function() {
            var queryObj = this.getQueryObj();
            delete(queryObj.simplify);
            var querystring = searchHelper.JSONToQueryString(queryObj);
            return this.paginator_core.url() + querystring.substring(1, querystring.length); 
        },
        'getCSVURL': function() {
            return this.getGeojsonURL() + "&format=csv";
        },
        'parse': function(res) {
            this.currentPage = parseInt(res.page);
            this.totalResults = parseInt(res.total);
            this.totalPages = parseInt(res.pages);
            var geojson = _.clone(res);
            mediator.commands.execute("map:loadSearchResults", geojson);
            return res.features;    
        },
        'unselectPlace': function(place) {
            if (this.contains(place)) {
                place.trigger('unselect');
                return;
            }    
            var id = place.id;
            var model = this.get(id);
            if (model) {
                model.trigger('unselect');
            }
            return;
        }
    });
    
    return Places;

});
