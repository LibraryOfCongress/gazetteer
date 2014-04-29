define(['Backbone', 'app/models/admin_boundary'], function(Backbone, AdminBoundary) {

    var AdminBoundaries = Backbone.Collection.extend({
        model: AdminBoundary
    });

    return AdminBoundaries; 

});
