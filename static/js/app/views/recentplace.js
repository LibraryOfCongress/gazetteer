define(['Backbone', 'marionette', 'underscore', 'text!app/views/recentplace.tpl'], function(Backbone, Marionette, _, template) {

    var RecentPlaceView = Marionette.ItemView.extend({
        template: _.template(template),
        tagName: 'li',
        events: {
            'click': 'openPlace'
        },

        openPlace: function() {
            var that = this;
            require(['app/core/mediator'], function(mediator) {
                mediator.commands.execute("openPlace", that.model);
            });
        }
    });

    return RecentPlaceView;
});
