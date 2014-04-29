define(['Backbone', 'marionette', 'underscore', 'app/views/origin', 'text!app/views/origins.tpl'], function(Backbone, Marionette, _, OriginView, template) {
    var OriginsView = Marionette.CompositeView.extend({
        template: _.template(template),
        className: 'origins',
        itemView: OriginView,
        events: {
            'click': 'stopPropagation',
            'click #clearOrigins': 'clearAll'
        },
        appendHtml: function(collectionView, itemView) {
            collectionView.$(".originsList").append(itemView.el);
        },
        clearAll: function(e) {
            e.preventDefault();
            this.collection.clearAll();
        },
        stopPropagation: function(e) {
            e.stopPropagation();
        }
 
    });

    return OriginsView;
});
