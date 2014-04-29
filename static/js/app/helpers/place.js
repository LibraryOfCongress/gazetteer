define([], function() {

    return {
        'getYear': function(dateString) {
            if (dateString.length > 4) {
                return dateString.substring(0,4);
            } else {
                return dateString;
            }    
        }
    }

});
