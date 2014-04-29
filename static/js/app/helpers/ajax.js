define(['require', 'jquery', 'app/core/mediator'], function(require, $, mediator) {

    var AjaxHelper = function() {
        this.csrftoken = getCookie('csrftoken');
        this.setupAjax = function() {
            
            var that = this;
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type)) {
                        // Send the token to same-origin, relative URLs only.
                        // Send the token only if the method warrants CSRF protection
                        // Using the CSRFToken value acquired earlier
                        xhr.setRequestHeader("X-CSRFToken", that.csrftoken);
                    }
                }
            });            
        };
        this.setupAjaxErrors = function() {
            $(document).ajaxError(function(e, xhr, settings, err) {
                if (xhr.status <= 200) { return; } //dont throw error modal if xhr was aborted in code
                if (xhr.getResponseHeader('Content-Type') === 'text/javascript') {
                    var opts = {
                        errorMsg: JSON.parse(xhr.responseText).error,
                        errorUrl: settings.url,
                        statusCode: xhr.status
                    };
                } else {
                    var opts = {
                        errorMsg: '',
                        errorUrl: settings.url,
                        statusCode: xhr.status
                    };
                }
                mediator.commands.execute("showModal", "error", opts);
                
            });

        };
        /*
        this.ajax = function(url, data, type, success_callback, error_callback) {

            $.ajax({
                url: url,
                type: type,
                dataType: 'json',
                data: data,
                success: success_callback,
                error: error_callback 

            });
        }; 
        */
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

    };

    return new AjaxHelper();
});
