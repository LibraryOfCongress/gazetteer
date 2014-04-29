define(['Backbone', 'app/models/place'], function(Backbone, Place) {
    var SimilarPlaces = Backbone.Collection.extend({
        model:  Place
    });

    return SimilarPlaces;
});
