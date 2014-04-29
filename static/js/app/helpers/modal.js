define(['require', 'jquery'], function(require, $) {

   var ModalHelper = function() {
        this.showModal = function(type, options) {
            //console.log("showModal", type, options);
            switch (type) {

                case "login":
                    require(['app/app', 'app/views/modals/login'], function(app, LoginView) {
                        var view = new LoginView();
                        app.modal.show(view);    
                    });
                    break;

                case "logout":
                    require(['app/app', 'app/views/modals/logout'], function(app, LogoutView) {
                        var view = new LogoutView();
                        app.modal.show(view);    
                    });
                    break;

                case "newPlace":
                    require(['app/app', 'app/views/modals/new_place'], function(app, NewPlaceView) {
                        var view = new NewPlaceView();
                        app.modal.show(view);
                    });
                    break;

                case "savePlace":
                    require(['app/app', 'app/views/modals/save_place'], function(app, SavePlaceView) {
                        var model = options.model;
                        var view = new SavePlaceView({'model': model});
                        app.modal.show(view);
                    });
                    break;

                case "revert":
                    require(['app/app', 'app/views/modals/revert_place'], function(app, RevertPlaceView) {
                        var view = new RevertPlaceView(options);
                        app.modal.show(view);
                    });
                    break;

                case "relate":
                    require(['app/app', 'app/views/modals/relate_places'], function(app, RelatePlacesView) {
                        var view = new RelatePlacesView(options);
                        app.modal.show(view);
                    });
                    break;

                case "delete_relation":
                    require(['app/app', 'app/views/modals/delete_relation'], function(app, DeleteRelationView) {
                        var view = new DeleteRelationView(options);
                        app.modal.show(view);
                    });
                    break;

                case "error":
                    if ($('#overlay').is(":visible")) {
                        this.closeModal();
                    }
                    require(['app/app', 'app/views/modals/error'], function(app, ErrorView) {
                        var view = new ErrorView(options);
                        app.modal.show(view);
                    });
                    break;

            }
            this.displayModal();
        };

        this.closeModal = function() {
            var that = this;
            require(['app/app', 'jquery'], function(app, $) {
                app.modal.close();
                $('#overlay').hide();
                that.removeCloseHandler();
            });
        };

        this.displayModal = function() {
            $('#overlay').show();
            this.addCloseHandler();
        };

        this.addCloseHandler = function() {
            var that = this;
            $('#overlay').on('click', function() {
                that.closeModal();
            });
            $('#lightBoxContent').on('click', function(e) {
                e.stopPropagation();
            });
            $(document).on('keyup', {'context': that}, this.closeOnEscape);
        };

        this.removeCloseHandler = function() {
            $('#overlay').off('click');
            $('#lightBoxContent').off('click');
            $(document).off('keyup', this.closeOnEscape);
        };

        this.closeOnEscape = function(e) {
            if (e.keyCode == 27) {
                e.data.context.closeModal();
            }
        };
    }; 

    return new ModalHelper();
});
