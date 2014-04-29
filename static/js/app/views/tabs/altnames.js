define(['Backbone', 'marionette', 'underscore', 'app/core/mediator', 'text!app/views/tabs/altnames.tpl', 'text!app/views/tabs/altnames_layout.tpl'], function(Backbone, Marionette, _, mediator, model_template, layout_template) {


    var AlternateNameView = Marionette.ItemView.extend({
        tagName: 'li',
        template: _.template(model_template),
        ui: {
           'altnameNameDetail': '.alternateNameName',
           'altnameLangDetail': '.alternateNameLang',
           'altnameTypeDetail': '.alternateNameType',
           'altnameNameInput': '.alternateNameNameInput',
           'altnameLangInput': '.alternateNameLangInput',
           'altnameTypeInput': '.alternateNameTypeInput',
           'editButtons': '.editButtons',
           'editButton': '.editAlternateName',
           'saveButtons': '.saveButtons',
           'saveButton': '.saveAlternateName',
           'details': '.altnameDetail',
           'editables': '.altnameEditable',
           'delete': '.deleteAlternateName'
        },
        events: {
            'click .editAlternateName': 'makeEditable',
            'click .saveAlternateName': 'save',
            'click .cancel': 'cancel',
            'click .deleteAlternateName': 'delete'
        },
        initialize: function() {
            this.bindUIElements();
            var that = this;
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
            this.ui.editButtons.show();    
        },
        hideEdit: function() {
            this.ui.editButtons.hide();
        },
        makeEditable: function() {
            this.ui.editButtons.hide();
            this.ui.saveButtons.show();
            this.ui.details.hide();
            this.ui.editables.show();
        },
        hideEditable: function() {
            this.ui.saveButtons.hide();
            this.ui.editButtons.show();
            this.ui.editables.hide();
            this.ui.details.show();
        },
        save: function() {
            var name = this.ui.altnameNameInput.val(),
                lang = this.ui.altnameLangInput.val(),
                type = this.ui.altnameTypeInput.val();
            this.model.set('name', name);
            this.model.set('lang', lang);
            this.model.set('type', type);
            this.ui.altnameNameDetail.text(name);
            this.ui.altnameLangDetail.text(lang);
            this.ui.altnameTypeDetail.text(type);
            this.hideEditable();
        },
        cancel: function() {
            if (this.model.isEmpty()) {
               this.remove();
                return; 
            }
            this.ui.altnameNameInput.val(this.ui.altnameNameDetail.text());
            this.ui.altnameLangInput.val(this.ui.altnameLangDetail.text());
            this.ui.altnameTypeInput.val(this.ui.altnameTypeDetail.text());
            this.hideEditable();
        },

        'delete': function() {
            this.model.clear();
            this.remove();
        }
    }); 

    var AlternateNamesView = Marionette.CollectionView.extend({
        tagName: 'ul',
        className: 'searchResultsList alternateNamesList',
        itemView: AlternateNameView
    });

    var AlternateNamesLayout = Marionette.Layout.extend({
        tagName: 'div',
        template: _.template(layout_template),
        regions: {
            'altnamesCollection': '.altnamesCollection'
        },
        ui: {
            'addButton': '.addAlternateName'
        },
        events: {
            'click .addAlternateName': 'addAlternateName'
        },
        initialize: function(options) {
            var that = this;
            this.collection = options.collection;
            this.model = options.model;
            mediator.events.on("login", function(user) {
                that.showEdit();        
            });
            mediator.events.on("logout", function() {
                that.hideEdit();
            });
        },
        onRender: function() {
            var collectionView = new AlternateNamesView({'collection': this.collection});
            this.altnamesCollection.show(collectionView);
            var user = mediator.requests.request("getUser");
            if (user) {
                this.showEdit();
            } else {
                this.hideEdit();
            }
        },
        showEdit: function() {
            this.ui.addButton.show();
        },
        hideEdit: function() {
            this.ui.addButton.hide();
        },
        addAlternateName: function() {
            var collection = this.collection;
            var newAltName = new collection.model();
            collection.add(newAltName);
            this.altnamesCollection.currentView.children.findByModel(newAltName).makeEditable();
        }
        

    });

    return AlternateNamesLayout;
}); 
