define(['Backbone', 'marionette', 'jquery', 'underscore', 'app/settings', 'app/core/mediator', 'app/collections/similar_places', 'text!app/views/tabs/similar_places.tpl', 'text!app/views/tabs/similar_place.tpl'], function(Backbone, Marionette, $, _, settings, mediator, SimilarPlaces, similarPlacesTemplate, similarPlaceTemplate) {
    
    var SimilarPlaceView = Marionette.ItemView.extend({
        tagName: 'tr',
        className: 'similarPlace',
        ui: {
            'relationText': '.relationText',
            'relationSelect': '.relationSelect',
            'editable': '.editable'    
        },
        events: {
            'mouseover': 'highlightPlace',
            'mouseout': 'unhighlightPlace',
            'change .relationSelect': 'makeRelation'
        },
        templateHelpers: function() {
            return {
                relationChoices: settings.relationChoices
            }    
        },
        template: _.template(similarPlaceTemplate),
        initialize: function() {
            this.listenTo(mediator.events, 'login', this.showEdit);
            this.listenTo(mediator.events, 'logout', this.hideEdit);
        },
        onRender: function() {
            var user = mediator.requests.request("getUser");
            if (user) {
                this.showEdit();
            } else {
                this.hideEdit();
            }
        },
        showEdit: function() {
            this.ui.editable.show();
            this.ui.relationText.hide();
        },
        hideEdit: function() {
            this.ui.editable.hide();
            this.ui.relationText.show();
        },
        highlightPlace: function() {
            mediator.commands.execute("map:highlight", this.model, "similarPlacesLayer");
        },
        unhighlightPlace: function() {
            mediator.commands.execute("map:unhighlight", this.model, "similarPlacesLayer");
        },
        updateRelation: function(relatedPlaces) {
            var that = this;
            _.each(relatedPlaces, function(relatedPlace) {
                if (relatedPlace.properties.id === that.model.id) {
                    that.ui.relationSelect.val(relatedPlace.properties.relation_type);
                    that.ui.relationText.text(relatedPlace.properties.relation_type);
                }
            });
        },
        makeRelation: function(e) {
            var relation_type = this.ui.relationSelect.val();
            var currentRelation = this.ui.relationText.text();
            this.ui.relationText.text(relation_type);
            var place1 = mediator.requests.request("getCurrentPlace");
            var place2 = this.model;
            var opts = {
                'place1': place1,
                'place2': place2,
                'relation': relation_type,
                'callee': 'similarPlaceView'
            }
            if (relation_type !== '') {
                mediator.commands.execute("showModal", "relate", opts);
            } else {
                opts.relation = currentRelation;
                mediator.commands.execute("showModal", "delete_relation", opts);
            }
        }
    });

    var SimilarPlacesView = Marionette.CompositeView.extend({
        tagName: 'table',    
        className: 'similarPlaces',
        template: _.template(similarPlacesTemplate),
        itemView: SimilarPlaceView,
        appendHtml: function(collectionView, itemView) {
            collectionView.$("tbody").append(itemView.el);
        },
        onRender: function() {
            var that = this;
            this.model.getSimilar(function(similarPlaces) {
                mediator.commands.execute("map:loadSimilar", similarPlaces);
            });
            this.model.getRelations(function(data) {
                that.children.each(function(childView) {
                    childView.updateRelation(data.features);
                });        
            });
        },
        onClose: function() {
            mediator.commands.execute("map:removeSimilar");
        }
    });

    return SimilarPlacesView;
});
