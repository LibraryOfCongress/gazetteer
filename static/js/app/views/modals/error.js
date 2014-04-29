define(['marionette', 'jquery', 'underscore', 'app/settings', 'app/core/mediator', 'text!app/views/modals/error.tpl'], function(Marionette, $, _, settings, mediator, template) {
    var ErrorView = Marionette.ItemView.extend({
        className: 'modalContent',
        template: _.template(template),
        initialize: function(options) {
            this.vars = options;
        },
        events: {

        },
        ui: {

        },
        serializeData: function() {
            return this.vars;
        },
        onRender: function() {
            var that = this;
            this.bindUIElements();
        }

    });    

    return ErrorView;
});
