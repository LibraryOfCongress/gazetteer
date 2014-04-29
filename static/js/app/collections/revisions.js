define(['Backbone', 'app/models/revision'], function(Backbone, Revision) {

    var Revisions = Backbone.Collection.extend({
        model: Revision
    });

    return Revisions; 

});
