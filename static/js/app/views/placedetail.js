define(['Backbone', 'marionette', 'jquery', 'underscore', 'app/settings', 'app/helpers/autocomplete', 'app/collections/revisions', 'app/core/mediator', 'text!app/views/placedetail.tpl', 'select2'], function(Backbone, Marionette, $, _, settings, autocompleteHelper, Revisions, mediator, template) {
    var PlaceDetailView = Marionette.Layout.extend({
        className: 'placeDetail',
        template: _.template(template),
        regions: {
            'tab': '#detailTabContainer',
            'recentPlaces': '.recentPlaces',
        },
        events: {
            'click .tabButton a': 'clickTab',
            'click .savePlaceBtn': 'save',
            'click .cancelSaveBtn': 'cancel',
            'click .editName': 'editName',
            'click .confirmEditName': 'confirmEditName',
            'click .cancelEditName': 'cancelEditName',
            'click .editFeatureType': 'editFeatureType',
            'click .confirmEditFeatureType': 'confirmEditFeatureType',
            'click .cancelEditFeatureType': 'cancelEditFeatureType',
            'click .editTimeframe': 'editTimeframe',
            'click .confirmEditTimeframe': 'confirmEditTimeframe',
            'click .cancelEditTimeframe': 'cancelEditTimeframe',
            'click .selectPlace': 'selectPlace'
        },
        ui: {
            'editButtons': '.editIcon',
            'saveButtons': '.saveButtons',
            'selectPlace': '.selectPlace',
            'featureTypeInput': '#editFeatureTypeInput',
            'lastUpdated': '.lastUpdated',
            'timeFrameStart': '#timeframe_start',
            'timeFrameStartRange': '#timeframe_start_range',
            'timeFrameEnd': '#timeframe_end',
            'timeFrameEndRange': '#timeframe_end_range'
        },
        initialize: function() {
            this.listenTo(mediator.events, 'login', this.showEdit);
            this.listenTo(mediator.events, 'logout', this.hideEdit);
            this.listenTo(this.model, 'change:properties', this.modelChanged);
            this.listenTo(this.model, 'change:geometry', this.modelChanged);
        },
        onRender: function() {
            var that = this;
            var user = mediator.requests.request("getUser");
            if (user) {
                this.showEdit();
            } else {
                this.hideEdit();
            }
            this.model.getRevisions(function(revs) {
                var revisions = new Revisions(revs);
                var mostRecent = revisions.last();
                var lastUpdated = mostRecent.getDisplayDate();
                that.ui.lastUpdated.text(lastUpdated);
            });
        },
        templateHelpers: function() {
            var that = this;
            return {
                isSelected: that.model.isSelected()
            }
        },

        selectPlace: function() {
            mediator.commands.execute("selectPlace", this.model);
        },

        placeSelected: function() {
            this.ui.selectPlace.hide();
        },

        placeUnselected: function() {
            this.ui.selectPlace.show();
        },

        showEdit: function() {
            this.ui.editButtons.show();
            this.ui.selectPlace.show();
        },
        hideEdit: function() {
            this.ui.editButtons.hide();
            this.ui.selectPlace.hide();
        },
        initFeatureTypeAutocomplete: function() {
            autocompleteHelper.initSelect2(this.ui.featureTypeInput, this.model);
        },
        destroyFeatureTypeAutocomplete: function() {
            autocompleteHelper.destroySelect2(this.ui.featureTypeInput);
        },
        modelChanged: function() {
            
            this.model.set('modelChanged', true);
            var saveVisible = this.ui.saveButtons.is(':visible');
            if (!saveVisible) {
                this.ui.saveButtons.show();
            } 
            this.save();
            
        },
        editName: function(e) {
            e.preventDefault();
            var $container = $('.editName').closest('.placeDetailEach');
            this.showEditable($container);
            var currentName = this.model.get('properties.name');
            $('#editNameInput').val(currentName);
        },
        showEditable: function($container) {
            $container.find('.placeDetailResult').hide();
            $container.find('.editable').show();
            $container.find('.editIcon').hide();
        },
        hideEditable: function($container) {
            $container.find('.placeDetailResult').show();
            $container.find('.editable').hide();
            $container.find('.editIcon').show();
        },
        confirmEditName: function(e) {
            e.preventDefault();
            var newName = $('#editNameInput').val();
            this.model.set('properties.name', newName);
            var $container = $('.editName').closest('.placeDetailEach');
            $container.find('.placeDetailResult').text(newName);
            this.hideEditable($container);
        },

        cancelEditName: function() {
            var $container = $('.editName').closest('.placeDetailEach');
            this.hideEditable($container);
        },

        editFeatureType: function(e) {
            e.preventDefault();
            var $container = $('.editFeatureType').closest('.placeDetailEach');
            this.showEditable($container);
            this.initFeatureTypeAutocomplete();
        },

        confirmEditFeatureType: function(e) {
            var $container = $('.editFeatureType').closest('.placeDetailEach');
            var featureTypeCode = this.ui.featureTypeInput.select2("val");
            var featureTypeName = this.model.get("currentFeatureName");
            this.model.set("properties.feature_code", featureTypeCode);
            this.model.set("properties.feature_code_name", featureTypeName);
            $container.find('.placeDetailResult').text(this.model.get("display.feature_type"));
            this.hideEditable($container);
            this.destroyFeatureTypeAutocomplete(); 
        },

        cancelEditFeatureType: function(e) {
            var $container = $('.editFeatureType').closest('.placeDetailEach');
            this.hideEditable($container);
            this.model.set("currentFeatureName", this.model.get("properties.feature_code_name"));
            this.destroyFeatureTypeAutocomplete();
        },

        editTimeframe: function(e) {
            e.preventDefault();
            var $container = $('.editTimeframe').closest('.placeDetailEach');
            this.showEditable($container);
            this.setTimeframeEditablesFromModel();
        },

        confirmEditTimeframe: function(e) {
            e.preventDefault();
            this.setModelFromTimeframeEditables();
            var $container = $('.editTimeframe').closest('.placeDetailEach');
            this.hideEditable($container);
            $container.find('.placeDetailResult').text(this.model.get('display.timeframe'));
        },

        cancelEditTimeframe: function() {
            var $container = $('.editTimeframe').closest('.placeDetailEach');
            this.hideEditable($container);
        },

        setTimeframeEditablesFromModel: function() {
            this.ui.timeFrameStart.val(this.model.get('properties.timeframe.start'));
            this.ui.timeFrameStartRange.val(this.model.get('properties.timeframe.start_range')), //FIXME: ranges need special handling?
            this.ui.timeFrameEnd.val(this.model.get('properties.timeframe.end'));
            this.ui.timeFrameEndRange.val(this.model.get('proprties.timeframe.end_range'));   

        },

        setModelFromTimeframeEditables: function() {
            var timeFrame = {
                start: this.ui.timeFrameStart.val(),
                start_range: this.ui.timeFrameStartRange.val(),
                end: this.ui.timeFrameEnd.val(),
                end_range: this.ui.timeFrameEndRange.val()
            };
            this.model.set('properties.timeframe', timeFrame);
        },

        save: function() {
            var that = this;
            require(['app/helpers/modal'], function(modalHelper) {
                //take variables from form and make changes to model
                var model = that.model;
                modalHelper.showModal("savePlace", {'model': model});
                
            });
        },
        cancel: function() {
            mediator.commands.execute("openPlace", this.model);
        },
        clickTab: function(e) {
            e.preventDefault()
            var $target = $(e.currentTarget);
            var tab = $target.attr("data-tab");
            this.showTab(tab);
        },
        showTab: function(tab) {
            var that = this;
            var app = require('app/app');
            var place = this.model;
            app.router.navigate(settings.app_base + 'place/' + place.id + '/' + tab, {'replace': true});
            var $button = this.$el.find('a[data-tab=' + tab + ']');
            this.$el.find('.active').removeClass("active");
            $button.parent().addClass("active");
            switch (tab) {

                case 'alternateNames':
                    require([
                        'app/views/tabs/altnames',
                        'app/collections/alternate_names',
                    ], function(AlternateNamesLayout, AlternateNamesCollection) {
                        var altNamesArr = place.get('properties.alternate');
                        if (!altNamesArr) {
                            altNamesArr = [];
                        }
                        var alternateNames = new AlternateNamesCollection(altNamesArr, {'place': that.model});
                        var view = new AlternateNamesLayout({'collection': alternateNames, 'model': that.model});
                        that.tab.show(view);
                    });
                    break;

                case 'revisions':
                    require([
                        'app/views/tabs/revisions',
                        'app/collections/revisions',
                    ], function(RevisionsView, RevisionsCollection) {
                        that.model.getRevisions(function(revisions) {
                            _.each(revisions, function(revision) {
                                revision.model_id = that.model.id;
                            });
                            var revisions = new RevisionsCollection(revisions);
                            var view = new RevisionsView({'collection': revisions});
                            that.tab.show(view);
                        }); 
                    });
                    break;

                case 'relations':
                    require([
                        'app/views/tabs/relations'
                    ], function(RelationsView) {
                        var view = new RelationsView({'model': that.model});
                        that.tab.show(view);
                    });
                    break;

                case 'adminBoundaries':
                    require([
                        'app/views/tabs/admin_boundaries',
                        'app/collections/admin_boundaries'
                    ], function(AdminBoundariesView, AdminBoundariesCollection) {
                        var admins = that.model.get('properties.admin');
                        if (!admins) {
                            var admins = [];
                        }
                        var admins = new AdminBoundariesCollection(admins);
                        var view = new AdminBoundariesView({'collection': admins});
                        that.tab.show(view);
                    });
                    break;

                case 'similarPlaces':
                    require([
                        'app/views/tabs/similar_places',
                        'app/collections/similar_places'
                    ], function(SimilarPlacesView, SimilarPlaces) {
                        that.model.getSimilar(function(data) {
                            var similarPlaces = new SimilarPlaces(data.features);
                            var view = new SimilarPlacesView({'collection': similarPlaces, 'model': that.model});
                            that.tab.show(view);
                        }); 

                    });
                    break;
            }
        }
    });

    return PlaceDetailView;

});
