define(['Backbone', 'marionette', 'underscore', 'app/settings', 'app/core/mediator', 'text!app/views/selectedplace.tpl'], function(Backbone, Marionette, _, settings, mediator, template) {

    var SelectedPlaceView = Marionette.ItemView.extend({
        template: _.template(template),
        tagName: 'tr',
        events: {
            'mouseover': 'mouseOverPlace',
            'mouseout': 'mouseOutPlace',
            'click .unselect': 'unselect',
            'click .relate': 'relatePlace',
            'change .relationType': 'showRelateModal'
        },
        ui: {
            'relate': '.relate',
            'makeRelation': '.makeRelation',
            'relatingFrom': '.relatingFrom',
            'relationType': '.relationType',
            'confirmRelationBtn': '.confirmRelationBtn'
        },

        initialize: function() {
            var app = require('app/app');
            this.isRelating = true;
            this.listenTo(app.collections.selectedPlaces, 'add', this.render);
            this.listenTo(app.collections.selectedPlaces, 'remove', this.render);
        },

        templateHelpers: function() {
            var app = require('app/app');
            return {
                'relationChoices': settings.relationChoices,
                'canRelate': app.collections.selectedPlaces.length > 1
            }    
        },

        openPlace: function(e) {
            var that = this;
            e.preventDefault();
            mediator.commands.execute("openPlace", that.model);
        },

        unselect: function(e) {
            e.preventDefault();
            mediator.commands.execute("unselectPlace", this.model);
            mediator.commands.execute("map:zoomToLayer", 'selectedPlacesLayer');
        },

        mouseOverPlace: function() {
            if (this.model.get("hasGeometry")) {
                mediator.commands.execute("map:highlight", this.model, 'selectedPlacesLayer');
            }
        },

        mouseOutPlace: function() {
            if (this.model.get("hasGeometry") && this.$el.is(":visible")) {
                mediator.commands.execute("map:unhighlight", this.model, 'selectedPlacesLayer');
            }
        },

        hideRelateBtn: function() {
            this.ui.relate.hide();
        },

        showRelateBtn: function() {
            this.ui.relate.show();
        },
        relateFrom: function(place, existingRelation) {
            this.ui.makeRelation.show();
            this.hideRelateBtn();
            this.hideRelateBtn();
            this.relatingFrom = {
                'place': place,
                'relation': existingRelation
            };
            this.ui.relatingFrom.text(place.get('properties.name'));
            if (existingRelation) {
                this.ui.relationType.val(existingRelation);
            } else {
                this.ui.relationType.val('');
            } 
        },

        stopRelateFrom: function(place) {
            this.relatingFrom = false;
            this.showRelateBtn();
            this.ui.makeRelation.hide();
        },

        relatePlace: function(e) {
            e.preventDefault();
            var app = require('app/app');
            this.$el.addClass('relatingPlace');
            this.isRelating = true;
            //this.hideRelateBtn();
            //this.showStopRelateBtn();
            app.views.selectedPlaces.trigger('relatePlace', this.model);
        },
        showRelateModal: function(e) {
            var relType = this.ui.relationType.val();
            var that = this;
            if (this.relatingFrom.relation != relType) {
                var opts = {
                    'place1': that.relatingFrom.place,
                    'place2': that.model,
                    'relation': relType,
                    'callee': 'selectedPlaceView'
                };
                if (relType != '') {
                    mediator.commands.execute("showModal", "relate", opts);
                } else {
                    mediator.commands.execute("showModal", "delete_relation", opts);
                }
                this.relatingFrom.relation = relType;
            }        
        },

        zoomOnMap: function(e) {
            e.preventDefault();
            mediator.commands.execute("map:zoomTo", this.model);
        }

    });

    return SelectedPlaceView;
});
