define(['Backbone', 'app/models/place'], function(Backbone, Place) {

    var ExistingRelations = Backbone.Collection.extend({
        model: Place,
        getRelation: function(place) {
            if (this.get(place.id)) {
                return this.get(place.id);
            }
            return false;    
        }

    });

    return ExistingRelations; 

});
