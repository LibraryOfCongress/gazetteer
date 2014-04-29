define(['marionette', 'jquery', 'underscore', 'app/core/mediator', 'app/settings', 'text!app/views/modals/login.tpl'], function(Marionette, $, _, mediator, settings, template) {
    var LoginView = Marionette.ItemView.extend({
        className: 'modalContent',
        template: _.template(template),
        events: {
            'submit #formLogin': 'submitForm'
        },
        ui: {
            'username': '#username',
            'password': '#password',
            'message': '.message'
        },
        onRender: function() {
            var that = this;
            this.bindUIElements();
            setTimeout(function() {
                that.ui.username.focus();
            }, 250);
        },

        submitForm: function(e) {
            e.preventDefault();
            var that = this;
            var username = this.ui.username.val();
            var password = this.ui.password.val();
            $.ajax({
                'type': 'POST',
                'dataType': 'json',
                'url': settings.app_base + 'login_json',
                'data': {
                    'username': username,
                    'password': password
                },
                'success': function(response) {
                    if (response.error) {
                        that.ui.message.text(response.error); 
                    } else {
                        mediator.events.trigger("login", response.user);
                        mediator.commands.execute("closeModal");
                    }
                }    
            });
        }    

    });    

    return LoginView;
});
