define(['Backbone'], function(Backbone) {

    var FeatureCode  = Backbone.Model.extend({
        idAttribute: 'typ',
        initialize: function() {
            this.set('checked', false);
        }
    });

    return FeatureCode;
});
