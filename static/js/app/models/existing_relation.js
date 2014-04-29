define(['Backbone', 'backbone_nested'], function(Backbone) {

    var ExistingRelation  = Backbone.NestedModel.extend({
        initialize: function() {
            this.id = this.get('properties.id');    
        }
    });

    return ExistingRelation;
});
