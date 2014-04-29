define(['marionette', 'Backbone', 'jquery', 'underscore', 'app/settings', 'app/core/mediator'], function(Marionette, Backbone, $, _, settings, mediator) {
    var NavigationView = Marionette.ItemView.extend({
        el: '#tabNavigation',

        ui: {
            'showResults': '.showResults',
            'showPlace': '.showPlace',
            'addPlaceBtn': '.addPlace',
            'selectedPlacesNumber': '#selectedPlacesNumber'
        },

        events: {
            'click .showResults': 'showResults',
            'click .showPlace': 'showPlace',
            'click .showSelected': 'showSelected',
            'click .addPlace': 'addPlace'
        },

        initialize: function() {
            var that = this;
            var app = require('app/app');
            this.bindUIElements();
            if (!_.isEmpty(app.user)) {
                this.showAddPlace();
            }
            this.listenTo(mediator.events, "selectTab", this.selectTab);
            this.listenTo(app.collections.selectedPlaces, 'add remove', this.updateSelectedNumber);
            this.listenTo(mediator.events, "login", this.showAddPlace);
            this.listenTo(mediator.events, "logout", this.hideAddPlace);
           
        },


        showResults: function() {
            if (this.getOpenTabName() === 'results') {
                return false;
            }
            var app = require('app/app');
            this.closeOpenTab();
            app.results.$el.addClass("activeContent").show();
            $(window).scrollTop(app.ui_state.resultsScroll);
            app.views.map.showResults();
            var searchURL = app.results.currentView.collection.getSearchURL();
            app.router.navigate(searchURL);
            this.selectTab('results');
        },

        showPlace: function() {
            if (this.getOpenTabName() === 'place') {
                return false;
            }
            var app = require('app/app');
            this.closeOpenTab();
            app.views.map.showPlace();
            app.placeDetail.$el.addClass("activeContent").show();
            var url = app.placeDetail.currentView.model.get("permalink");
            app.router.navigate(url);
            this.selectTab('place');
        },

        updateSelectedNumber: function() {
            var app = require('app/app');
            var selectedNumber = app.collections.selectedPlaces.length;
            this.ui.selectedPlacesNumber.text(selectedNumber);
        },

        showSelected: function() {
            if (this.getOpenTabName() === 'selected') {
                return false;
            }
            var app = require('app/app');
            this.closeOpenTab();
            app.views.map.showSelectedPlaces();
            app.selectedPlaces.$el.addClass("activeContent").show();
            var url = settings.app_base + "selected";
            app.router.navigate(url);
            this.selectTab('selected');
        },

        closeOpenTab: function() {
            var app = require('app/app');
            var openTabName = this.getOpenTabName();
            if (openTabName === 'results') {
                app.ui_state.resultsScroll = $(window).scrollTop();
            }
            $('.activeContent').removeClass('activeContent').hide();
        },
       
        getOpenTabName: function() {
            return this.$el.find('.activeNav').attr("data-name");        
        }, 

        unselectCurrent: function() {
            this.$el.find('.activeNav').removeClass('activeNav');
        },


        getTab: function(name) {
            return this.$el.find('.tabButton[data-name=' + name + ']');
        },

        showTab: function(name) {
            var $tab = this.getTab(name);
            $tab.show();
        },

        hideTab: function(name) {
            var $tab = this.getTab(name);
            $tab.hide();
        },

        selectTab: function(name) {
            var $tab = this.getTab(name);
            if (!$tab.is(":visible")) {
                $tab.show();
            }
            this.unselectCurrent();
            $tab.addClass('activeNav');
        },

        showAddPlace: function() {
            this.ui.addPlaceBtn.show();
        },
        
        hideAddPlace: function() {
            this.ui.addPlaceBtn.hide();
        },

        addPlace: function(e) {
            e.preventDefault();
            mediator.commands.execute("showModal", "newPlace");
        } 

    });
    
    return NavigationView;
});
