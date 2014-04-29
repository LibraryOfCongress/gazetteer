define(['Backbone', 'marionette', 'underscore', 'app/core/mediator', 'app/helpers/autocomplete', 'app/views/feature_code', 'text!app/views/feature_codes.tpl'], function(Backbone, Marionette, _, mediator, autocompleteHelper, FeatureCodeView, template) {
    var FeatureCodesView = Marionette.CompositeView.extend({
        template: _.template(template),
        className: 'featureCodes',
        itemView: FeatureCodeView,
        events: {
            'click': 'stopPropagation',
            'click #clearFcodes': 'clearAll'
        },
        ui: {
            'addFeatureCode': '#addFeatureCode'
        },
        appendHtml: function(collectionView, itemView) {
            collectionView.$(".fcodesList").append(itemView.el);
        },
        onRender: function() {
            var $elem = autocompleteHelper.initSelect2(this.ui.addFeatureCode);
            $elem.on("fcodeChanged", function(e, fcode) {
                mediator.commands.execute("search:addFeatureCode", fcode);
            });
        },
        onClose: function() {
            autocompleteHelper.destroySelect2(this.ui.addFeatureCode);
        },
        clearAll: function(e) {
            e.preventDefault();
            this.collection.clearAll();
        },
        stopPropagation: function(e) {
            e.stopPropagation();
        }
 
    });

    return FeatureCodesView;
});
