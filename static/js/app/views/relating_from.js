define(['Backbone', 'marionette', 'underscore', 'app/core/mediator', 'text!app/views/relating_from.tpl'], function(Backbone, Marionette, _, mediator, template) {
    var RelatingFromView = Marionette.ItemView.extend({
        template: _.template(template),
        className: 'relatingFromView',
        events: {
            'click .stopRelating': 'stopRelating' 
        },
        onRender: function() {
            mediator.commands.execute("map:highlight", this.model, "selectedPlacesLayer");
        },
        onClose: function() {
            mediator.commands.execute("map:unhighlight", this.model, "selectedPlacesLayer");
        },
        stopRelating: function(e) {
            e.preventDefault();
            var app = require('app/app');
            app.views.selectedPlaces.trigger('stopRelatePlace', this.model);
        }
        
    });

    return RelatingFromView;
});
