define(['Backbone'], function(Backbone) {

    var Origin  = Backbone.Model.extend({
        initialize: function() {
            this.set('checked', false);
        }
    });

    return Origin;
});
