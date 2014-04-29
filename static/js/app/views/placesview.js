define(['Backbone', 'marionette', 'underscore', 'jquery', 'app/core/mediator', 'app/views/placeview', 'text!app/views/placesview.tpl'], function(Backbone, Marionette, _, $, mediator, PlaceView, template) {

    var PlacesView = Marionette.CompositeView.extend({
        'template': _.template(template),
        //'el': '#searchResultsBlock',
        'tagName': 'table',
        'className': 'searchResultsTable',
        'initialize': function() {
            var that = this;
            this.listenTo(mediator.events, "clickedPlace", function(place) {
                that.children.each(function(childView) {
                    if (childView.iconsDisplayed && childView.model.id !== place.id) {
                        childView.hideIcons();
                    }
                });
            });
        },
        //'className': 'searchResultsList',
        'itemView': PlaceView,
        'appendHtml': function(collectionView, itemView) {
            collectionView.$("tbody").append(itemView.el);    
        }
    });

    return PlacesView;
});
