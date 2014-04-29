define(['marionette', 'Backbone', 'jquery', 'underscore', 'app/core/mediator'], function(Marionette, Backbone, $, _, mediator) {
    var HeaderView = Marionette.ItemView.extend({
        //template: _.template(mapTemplate),
        el: '#siteHeader',
        ui: {
            'searchLink': '#searchLink',
            'loginButtons': '.loginButtons',
            'loggedInMsg': '.loggedInMsg',
            'logoutBtn': '.logoutBtn',
            'loggedInBlock': '.loggedInBlock'
        },
        events: {
            // 'click #searchLink': 'toggleSearch',
            'click #loginBtn': 'openLoginModal',
            'click #logoutBtn': 'openLogoutModal'
        },

        initialize: function() {
            var that = this;
            this.bindUIElements();
            var user = mediator.requests.request("getUser");
            if (user) {
                this.loginUser(user);
            }
            this.listenTo(mediator.events, 'login', this.loginUser);
            this.listenTo(mediator.events, 'logout', this.logoutUser);
        },

/*        toggleSearch: function() {
            //console.log("toggle search");
            $('#searchToggleBlock').slideToggle();
        },
*/
        openLoginModal: function(e) {
            e.preventDefault();
            mediator.commands.execute("showModal", "login");    
        },

        openLogoutModal: function(e) {
            e.preventDefault();
            mediator.commands.execute("showModal", "logout");
        },

        loginUser: function(user) {
            this.ui.loginButtons.hide();
            this.ui.loggedInMsg.text(user.username);
            this.ui.loggedInBlock.show();     
        },
        logoutUser: function() {
            this.ui.loginButtons.show();
            this.ui.loggedInMsg.text('');
            this.ui.loggedInBlock.hide();
        }
/*
        hideSearch: function() {
            $('#searchToggleBlock').slideUp();
        },

        showSearch: function() {
            $('#searchToggleBlock').slideDown();
        }
*/
    });
    
    return HeaderView;
});
