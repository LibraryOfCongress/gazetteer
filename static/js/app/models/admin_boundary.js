define(['Backbone', 'app/settings'], function(Backbone, settings) {

    var AdminBoundary  = Backbone.Model.extend({
        initialize: function() {
            this.set('url', this.getURL());
            if (typeof(this.get('alternate_names')) == 'undefined') {
                this.set('alternate_names', []);
            }
        },

        getURL: function() {
            if (this.get('id')) {
                return '#detail/' + this.get('id');
            }
            return false;
        }
    });

    return AdminBoundary;
});
