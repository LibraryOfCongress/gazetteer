define(['Backbone', 'marionette', 'underscore', 'text!app/views/feature_code.tpl'], function(Backbone, Marionette, _, template) {

    var FeatureCodeView = Marionette.ItemView.extend({
        template: _.template(template),
        tagName: 'li',
        events: {
            'change .fcodeCheckbox': 'setFcodeChecked'
        },
        initialize: function() {
            this.listenTo(this.model, 'change:checked', this.render);
        },
        setFcodeChecked: function(e) {
            var $checkbox = $(e.target);
            if ($checkbox.is(":checked")) {
                this.model.set('checked', true);
            } else {
                this.model.set('checked', false);
            }
        }

    });

    return FeatureCodeView;
});
