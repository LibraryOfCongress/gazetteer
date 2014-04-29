define(['Backbone', 'marionette', 'underscore', 'text!app/views/origin.tpl'], function(Backbone, Marionette, _, template) {

    var OriginView = Marionette.ItemView.extend({
        template: _.template(template),
        tagName: 'li',
        events: {
            'change .originCheckbox': 'setOriginChecked'
        },
        initialize: function() {
            this.listenTo(this.model, 'change:checked', this.render);
        },
        setOriginChecked: function(e) {
            var $checkbox = $(e.target);
            if ($checkbox.is(":checked")) {
                this.model.set('checked', true);
            } else {
                this.model.set('checked', false);
            }
        }

    });

    return OriginView;
});
