define(['Backbone', 'underscore', 'app/models/origin'], function(Backbone, _, Origin) {

    var Origins = Backbone.Collection.extend({
        model: Origin,
        getChecked: function() {
            var checkedOrigins = [];
            this.each(function(origin) {
                if (origin.get('checked')) {
                    checkedOrigins.push(origin);
                }    
            });
            return checkedOrigins;
        },
        getQueryString: function() {
            var checkedOrigins = this.getChecked();
            var checkedOriginCodes = _.map(checkedOrigins, function(origin) {
                return origin.get('code');
            });
            return window.encodeURIComponent(checkedOriginCodes.join("|"));
        },
        clearAll: function() {
            this.each(function(origin) {
                origin.set('checked', false);
            });
        },
        markFromQuery: function(qstring) {
            var codes = window.decodeURIComponent(qstring).split('|');
            this.clearAll();
            this.each(function(origin) {
                _.each(codes, function(code) {
                    if (code === origin.get('code')) {
                        origin.set('checked', true);
                    }
                });
            });
        }
    });

    return Origins; 

});
