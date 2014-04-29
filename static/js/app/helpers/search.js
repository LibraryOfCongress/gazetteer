define(['Backbone', 'jquery', 'app/core/mediator', 'app/settings', 'require'], function(Backbone, $, mediator, settings, require) {
    var SearchHelper = function() {
        
        this.queryStringToJSON = function(qstring) {
            if (qstring.indexOf("?") == -1) {
                return {};
            }
            var q = qstring.split("?")[1];
            var args = {};
            var vars = q.split('&');
            for (var i=0; i<vars.length; i++) {
                var kv = vars[i].split('=');
                var key = kv[0];
                var value = kv[1];
                args[key] = value;
            }		
            return args; 
        };

        this.JSONToQueryString = function(obj) {
            var s = "?";
            for (var o in obj) {
                if (obj.hasOwnProperty(o) && obj[o] !== '') {
                    s += o + "=" + obj[o] + "&";
                }
            }
            return s.substring(0, s.length - 1);
        };

        this.getSearchParams = function() {
            var app = require("app/app");
            var params = app.views.search.getSearchParams();
            if (params.searchInBBox) {
                params.bbox = app.views.map.getBBoxString();
            }
            delete(params.searchInBBox);
            params.origins = app.collections.origins.getQueryString();
            params.feature_codes = app.collections.featureCodes.getQueryString();
            return params;
        };

        this.getSearchURL = function() {
            var searchObj = this.getSearchParams();
            return settings.app_base + "search" + this.JSONToQueryString(searchObj);
        };

        this.getOriginQuery = function(originsString) {
            var originsArr = window.decodeURIComponent(originsString).split('|');
            var searchQueries = _.map(originsArr, function(o) {
                return "*" + o + "*";
            });
            return 'uris:(' + searchQueries.join(' OR ') + ')';
        };

        this.getFeatureCodeQuery = function(featureCodesString) {
            var featureCodesArr = window.decodeURIComponent(featureCodesString).split('|');
            return 'feature_code:(' + featureCodesArr.join(' OR ') + ')';
        };
    };        

    return new SearchHelper();

});
