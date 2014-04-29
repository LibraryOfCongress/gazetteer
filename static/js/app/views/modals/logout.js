define(['marionette', 'jquery', 'underscore', 'app/settings', 'app/core/mediator', 'text!app/views/modals/logout.tpl'], function(Marionette, $, _, settings, mediator, template) {
    var LogoutView = Marionette.ItemView.extend({
        className: 'modalContent',
        template: _.template(template),
        events: {
            'click .confirmLogout': 'confirm',
            'click .cancelLogout': 'cancel'
        },
        ui: {
            'confirmiLogout': '.confirm',
            'cancelLogout': '.cancel'    
        },
        onRender: function() {
            var that = this;
            this.bindUIElements();
        },

        confirm: function(e) {
            e.preventDefault();
            var that = this;
            $.ajax({
                'type': 'POST',
                'dataType': 'json',
                'url': settings.app_base + 'logout_json',
                'data': {},
                'success': function(response) {
                    mediator.events.trigger("logout");
                    mediator.commands.execute("closeModal");
                }

            });
        },
        cancel: function(e) {
            e.preventDefault();
            mediator.commands.execute("closeModal");
        }    

    });    

    return LogoutView;
});
