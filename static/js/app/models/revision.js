define(['Backbone', 'moment', 'app/settings'], function(Backbone, moment, settings) {

    var Revision  = Backbone.Model.extend({

        initialize: function() {
            var model_id = this.get('model_id');
            var digest = this.get('digest');
            this.set('displayDate', this.getDisplayDate());
            this.set('revisionURL', settings.api_base + 'place/' + model_id + '/' + digest + ".json");
        },
        getDisplayDate: function() {
            var created_at = parseFloat(this.get('created_at'));
            return moment(created_at * 1000).format("MMMM Do YYYY, h:mm:ss a");
        }

    });

    return Revision;
});
