define(['Backbone'], function(Backbone) {

    var AlternateName = Backbone.Model.extend({
        defaults: {
            'name': '',
            'lang': '',
            'type': ''
        },
        initialize: function() {
            if (typeof(this.get('type')) == 'undefined') {
                this.set('type', '');
            }
        },
        isEmpty: function() {
            return (typeof(this.get('name')) == 'undefined' || this.get('name') === '');
        }

    });

    return AlternateName;
});
