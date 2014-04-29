define(['Backbone', 'underscore', 'app/models/alternate_name'], function(Backbone, _, AlternateName) {

    var AlternateNames = Backbone.Collection.extend({
        model: AlternateName,
        initialize: function(arr, options) {
            var place = options.place;
            //console.log("altnames place", place);
            this.on("change", function() {
                var altnames = this.toJSON();
                //console.log("place", place);
                console.log("altnames changed", altnames);
                var allProps = place.get('properties');
                //console.log('all props', allProps);
                allProps.alternate = altnames;
                place.set('properties', allProps);
                place.trigger('change:properties');
            });
        },
        toJSON: function() {
            var ret = [];
            _.each(this.models, function(model) {
                if (!model.isEmpty()) {
                    ret.push(model.toJSON());
                } 
            });
            return ret;
        }
    });

    return AlternateNames; 

});
