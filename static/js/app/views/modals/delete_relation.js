define(['marionette', 'jquery', 'underscore', 'app/app', 'app/core/mediator', 'app/settings', 'text!app/views/modals/delete_relation.tpl'], function(Marionette, $, _, app, mediator, settings, template) {
    var DeleteRelationView = Marionette.ItemView.extend({
        className: 'modalContent',
        template: _.template(template),
        events: {
            'submit #deleteRelationForm': 'submitForm'
        },
        initialize: function(options) {
            this.place1 = options.place1;
            this.place2 = options.place2;
            this.relation = options.relation;
            this.callee = options.callee ? options.callee : '';
        },
        ui: {
            'comment': '#relateComments',
            'message': '.message'
        },
        onRender: function() {
            var that = this;
            this.bindUIElements();
            setTimeout(function() {
                that.ui.comment.focus();
            }, 250);
        },
        serializeData: function() {
            var that = this;
            return {
                'place1_name': that.place1.get('properties.name'),
                'place2_name': that.place2.get('properties.name'),
                'relation': that.relation
            }
        },
        submitForm: function(e) {
            e.preventDefault();
            var that = this;
            var comment = this.ui.comment.val();
            var data = JSON.stringify({'comment': comment});
            var url = settings.api_base + 'place/' + this.place1.id + '/' + this.relation + '/' + this.place2.id + '.json';
            $.ajax({
                'type': 'DELETE',
                'dataType': 'json',
                'url': url,
                'data': data,
                'success': function(response) {
                    if (response.error) {
                        that.ui.message.text(response.error); 
                    } else {
                        that.place1.fetch();
                        that.place1.set('relations', false);
                        if (that.callee == 'relationView' && mediator.requests.request("getCurrentPlace").id == that.place1.id) {
                            var placeDetailView = app.placeDetail.currentView;
                            placeDetailView.showTab('relations');  
                        }
                        mediator.commands.execute("closeModal");
                    }
                }    
            });
        }    

    });    

    return DeleteRelationView;
});
