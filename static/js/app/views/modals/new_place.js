define(['marionette', 'jquery', 'underscore', 'app/core/mediator', 'app/settings', 'app/helpers/autocomplete', 'text!app/views/modals/new_place.tpl'], function(Marionette, $, _, mediator, settings, autocompleteHelper, template) {
    var NewPlaceView = Marionette.ItemView.extend({
        className: 'modalContent',
        template: _.template(template),
        events: {
            'submit #newPlaceForm': 'submitForm'
        },
        ui: {
            'name': '#newPlaceName',
            'type': '#newPlaceType',
            'isComposite': '#isComposite',
            'message': '.message'
        },
        onRender: function() {
            var that = this;
            this.bindUIElements();
            setTimeout(function() {
                that.ui.name.focus();
            }, 250);
            autocompleteHelper.initSelect2(this.ui.type);
        },
        onClose: function() {
            autocompleteHelper.destroySelect2(this.ui.type);
        },
        submitForm: function(e) {
            e.preventDefault();
            var that = this;
            var name = this.ui.name.val();
            var type = this.ui.type.val();
            var isComposite = this.ui.isComposite.is(":checked");
            var placeGeoJSON = {
                "geometry": {},
                "type": "Feature",
                "properties": {
                    "importance": null,
                    "feature_code": type,
                    "id": null,
                    "population": null,
                    "is_composite": isComposite,
                    "name": name,
                    "area": null,
                    "admin": [],
                    "is_primary": true,
                    "alternate": null,
                    "feature_code_name": "", 
                    "timeframe": {}, 
                    "uris": []
                }
            };
            var data = JSON.stringify(placeGeoJSON);
            $.ajax({
                'type': 'POST',
                'dataType': 'json',
                'url': settings.api_base + 'place.json',
                'data': data,
                'success': function(response) {
                    if (response.error) {
                        that.ui.message.text(response.error); 
                    } else {
                        require(['app/models/place'], function(Place) {
                            var place = new Place(response);
                            mediator.commands.execute("closeModal");
                            mediator.commands.execute("openPlace", place);
                        });
                    }
                }    
            });
        }    

    });    

    return NewPlaceView;
});
