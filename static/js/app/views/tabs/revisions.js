define(['Backbone', 'marionette', 'underscore', 'app/core/mediator', 'text!app/views/tabs/revisions.tpl'], function(Backbone, Marionette, _, mediator, template) {


    var RevisionView = Marionette.ItemView.extend({
        tagName: 'li',
        template: _.template(template),
        events: {
            'click .revert': 'revert',
            'click .viewDiff': 'viewDiff'
        },
        ui: {
            'revertBtn': '.revert',
            'revertDisplay': '.revertDisplay'
        },
        initialize: function() {
            this.isLast = false;
            this.listenTo(mediator.events, 'login', this.showRevert);
            this.listenTo(mediator.events, 'logout', this.hideRevert);
        },
        onRender: function() {
            var user = mediator.requests.request("getUser");
            if (user) {
                this.showRevert();
            } else {
                this.hideRevert();
            }
        },
        showRevert: function() {
            if (!this.isLast) {
                this.ui.revertDisplay.show();
            }
        },
        hideRevert: function() {
            this.ui.revertDisplay.hide();
        },
        markLast: function() {
            this.isLast = true;
            this.hideRevert();
        },
        revert: function(e) {
            e.preventDefault();
            var that = this;
            require(['app/helpers/modal'], function(modalHelper) {
                var revision = that.model;
                var place = mediator.requests.request("getCurrentPlace");
                modalHelper.showModal("revert", {
                    'revision': revision,
                    'place': place
                });
            });
        },
        viewDiff: function(e) {
            e.preventDefault();
        }
        
    }); 

    var RevisionsView = Marionette.CollectionView.extend({
        tagName: 'ol',
        className: 'reverseOrderedList smallFont',
        itemView: RevisionView,
        onRender: function() {
            if (this.children.length > 0) {
                var lastItem = this.children.last();
                lastItem.markLast();   
            }
        }
    });

    return RevisionsView;
}); 
