define(['Backbone', 'marionette', 'underscore', 'app/views/selectedplace', 'text!app/views/selectedplaces.tpl'], function(Backbone, Marionette, underscore, SelectedPlace, template) {
    var SelectedPlacesView = Marionette.CompositeView.extend({
        itemView: SelectedPlace,
        tagName: 'table',
        template: _.template(template),
        className: 'selectedPlaces searchResultsTable',
        appendHtml: function(collectionView, itemView) {
            collectionView.$("tbody").append(itemView.el);
        },
    });

    return SelectedPlacesView;

});
