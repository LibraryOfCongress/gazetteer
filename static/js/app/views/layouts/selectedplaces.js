define(['Backbone', 'marionette', 'underscore', 'jquery', 'app/core/mediator', 'app/collections/existing_relations', 'app/views/selectedplaces', 'text!app/views/layouts/selectedplaces.tpl'], function(Backbone, Marionette, _, $, mediator, ExistingRelations, SelectedPlacesView, template) {
    var SelectedPlacesLayout = Marionette.Layout.extend({
        template: _.template(template),
        initialize: function(options) {
            var that = this;
            this.selectedCollection = options.selectedCollection;
            this.listenTo(this.selectedCollection, 'add', function() {
                if (that.selectedCollection.length == 1) {
                    that.showTab();
                }    
            });
            this.listenTo(this, 'relatePlace', this.relate);
            this.listenTo(this, 'stopRelatePlace', this.stopRelate);
        },
        regions: {
            'places': '#selectedPlacesBlock',
            'placeRelatingFrom': '#placeRelatingFrom'
        },
        events: {
            'click .zoomToLayer': 'zoomToLayer'       
        },

        showTab: function() {
            mediator.commands.execute("nav:showTab", "selected");
        },

        hideTab: function() {
            mediator.commands.execute("nav:hideTab", "selected");
            
        },

        relate: function(model) {
            var that = this;
            require(['app/views/relating_from'], function(RelatingFromView) {
                var relatingFromView = new RelatingFromView({'model': model});
                that.placeRelatingFrom.show(relatingFromView);
                model.getRelations(function(relations) {
                    var collectionView = that.places.currentView;
                    var relationsCollection = new ExistingRelations(relations.features);
                    collectionView.children.each(function(itemView) {
                        var thisModel = itemView.model;
                        if (thisModel.id !== model.id) {
                            if (!itemView.$el.is(":visible")) {
                                itemView.$el.show();
                            }
                            var existingRelation = relationsCollection.getRelation(thisModel);
                            itemView.relateFrom(model, existingRelation ? existingRelation.get('properties.relation_type') : false); 
                        } else {
                            itemView.$el.hide();
                        }
                    });
                });
            });
        },

        stopRelate: function(model) {
            var collectionView = this.places.currentView;
            this.placeRelatingFrom.close();
            collectionView.children.each(function(itemView) {
                var thisModel = itemView.model;
                if (thisModel.id !== model.id) {
                    itemView.stopRelateFrom(model);
                } else {
                    itemView.$el.show();
                }
            });
        },

        onRender: function() {
            var selectedPlacesView = new SelectedPlacesView({'collection': this.selectedCollection});
            this.places.show(selectedPlacesView);
        },

        zoomToLayer: function() {
            mediator.commands.execute("map:zoomToLayer", "selectedPlacesLayer");
        }
    });

    return SelectedPlacesLayout;
});
