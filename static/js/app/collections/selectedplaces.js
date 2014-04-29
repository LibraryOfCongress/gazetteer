define(['Backbone', 'app/models/place'], function(Backbone, Place) {
    var SelectedPlaces = Backbone.Collection.extend({
        model:  Place,
        removePlace: function(place) {
            if (this.contains(place)) {
                this.remove(place);
                return;
            }
            var model = this.get(place.id);
            if (model) {
                this.remove(model);
                return;
            }
            return;
        }
    });

    return SelectedPlaces;
});
