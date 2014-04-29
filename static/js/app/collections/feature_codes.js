define(['Backbone', 'underscore', 'app/models/feature_code'], function(Backbone, _, FeatureCode) {

    var FeatureCodes = Backbone.Collection.extend({
        model: FeatureCode,
        getChecked: function() {
            var checkedFeatureCodes = [];
            this.each(function(featureCode) {
                if (featureCode.get('checked')) {
                    checkedFeatureCodes.push(featureCode);
                }    
            });
            return checkedFeatureCodes;
        },
        getQueryString: function() {
            var checkedFeatureCodes = this.getChecked();
            var checkedFeatureCodeTypes = _.map(checkedFeatureCodes, function(featureCode) {
                return featureCode.get('typ');
            });
            return window.encodeURIComponent(checkedFeatureCodeTypes.join("|"));
        },
        clearAll: function() {
            this.each(function(featureCode) {
                featureCode.set('checked', false);
            });
        },
        markFromQuery: function(qstring) {
            var typs = window.decodeURIComponent(qstring).split('|');
            this.clearAll();
            this.each(function(featureCode) {
                _.each(typs, function(typ) {
                    if (typ === featureCode.get('typ')) {
                        featureCode.set('checked', true);
                    }
                });
            });
        }
    });

    return FeatureCodes; 

});
