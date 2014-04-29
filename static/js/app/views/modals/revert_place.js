define(['marionette', 'jquery', 'underscore', 'app/core/mediator', 'text!app/views/modals/revert_place.tpl'], function(Marionette, $, _, mediator, template) {
    var RevertPlaceView = Marionette.ItemView.extend({
        className: 'modalContent',
        template: _.template(template),
        events: {
            'submit #revertPlaceForm': 'submitForm'
        },
        initialize: function(options) {
            this.revision = options.revision;
            this.place = options.place;
        },
        ui: {
            'comment': '#revertComments',
            'message': '.message'
        },
        onRender: function() {
            var that = this;
            this.bindUIElements();
            setTimeout(function() {
                that.ui.comment.focus();
            }, 250);
        },
        submitForm: function(e) {
            e.preventDefault();
            var that = this;
            var comment = this.ui.comment.val();
            var data = JSON.stringify({'comment': comment});
            var url = this.revision.get('revisionURL');
            $.ajax({
                'type': 'PUT',
                'dataType': 'json',
                'url': url,
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

    return RevertPlaceView;
});
