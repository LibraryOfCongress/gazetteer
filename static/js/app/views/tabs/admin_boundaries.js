define(['Backbone', 'marionette', 'underscore', 'app/core/mediator', 'text!app/views/tabs/admin_boundaries.tpl'], function(Backbone, Marionette, _, mediator, template) {


    var AdminBoundaryView = Marionette.ItemView.extend({
        tagName: 'li',
        template: _.template(template),
        events: {
            'click .openPlace': 'openPlace'
        },
        openPlace: function(e) {
            e.preventDefault();
            mediator.commands.execute("getPlaceAsync", this.model.get('id'), function(place) {
                mediator.commands.execute("openPlace", place);
            });
        }
    }); 

    var AdminBoundariesView = Marionette.CollectionView.extend({
        tagName: 'ul',
        className: 'searchResultsList adminBoundariesList',
        itemView: AdminBoundaryView
    });

    return AdminBoundariesView;
}); 
