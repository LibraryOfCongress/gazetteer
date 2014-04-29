define(['Backbone', 'app/models/place'], function(Backbone, Place) {
    var RecentPlaces = Backbone.Collection.extend({
        model:  Place
    });

    return RecentPlaces;
});
