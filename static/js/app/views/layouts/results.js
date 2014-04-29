define(['Backbone', 'marionette', 'underscore', 'jquery', 'app/core/mediator', 'text!app/views/layouts/results.tpl'], function(Backbone, Marionette, _, $, mediator, template) {
    var ResultsLayout = Marionette.Layout.extend({
        template: _.template(template),
        initialize: function(options) {
            this.collection = options.collection;
        },
        regions: {
            'places': '#searchResultsBlock',
            'pagination': '#paginationBlock',
            'recentPlaces': '.recentPlaces'
        },
        events: {
            'click .zoomToLayer': 'zoomToLayer'
        },

        serializeData: function() {
            return {
                'queryString': this.collection.server_api.q,
                'geojsonURL': this.collection.getGeojsonURL(),
                'csvURL': this.collection.getCSVURL()
            }
        },
        onRender: function() {
            var that = this;
            require(['app/views/placesview'], function(PlacesView) {
                var placesView = new PlacesView({'collection': that.collection});
                that.places.show(placesView);
            });
            require(['app/views/pagination'], function(PaginationView) {
                var paginationView = new PaginationView({'collection': that.collection});
                that.pagination.show(paginationView);
            });
        },
        zoomToLayer: function() {
            mediator.commands.execute("map:zoomToLayer", "resultsLayer");
        }
    });

    return ResultsLayout;
});
