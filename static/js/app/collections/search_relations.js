define(['Backbone', 'app/collections/places', 'app/models/search_relation'], function(Backbone, Places, SearchRelation) {

    var SearchRelations = Places.extend({
        model: SearchRelation,
        parse: function(data) {
            return data.features;
        }
    });

    return SearchRelations; 

});
