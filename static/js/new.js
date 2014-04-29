'use strict';

var map, jsonLayer;

var API_URL = $G.apiBase.slice(0, -1)  + ".json";
//* `POST /place.json
$(function() {
    

    var featureCodeValue = $('#featureCode').val();   
    $('#featureCode').select2({
        ajax: {
            'url': $G.apiBase + "feature_codes.json",
            dataType: 'json',
            quietMillis: 100,
            data: function(term, page) {
                return {
                    q: term,
                    page_limit: 10,
                    page: page
                }
            },
            results: function(data, page) {
                var more = data.has_next;
                return {results: data.items, more: more};
            }
        },
        formatResult: function(item) {
            return "<div>" + item.cls + ":" + item.typ + " " + item.name + "<div style='font-size:12px'><i>" + item.description + "</i></div></div>"
        },
        formatSelection: function(item) {
            return item.typ;           
            //return "<div data-id='" + item.id + "'>" + item.first_name + " " + item.last_name + "</div>";
        },
        initSelection: function(elem, callback) {
            var val = $(elem).val();
            var data = {
                'id': featureCodeValue,
                'typ': featureCodeValue
            };
            callback(data); 
        }
    });
    

    $('#placeForm').submit(function(e) {
        e.preventDefault();
        
        var data = {
            'name': $('#placeName').val(),
            'feature_code': $('#featureCode').val(),
            'is_composite': $("#is_composite").is(":checked")
        };
        $.extend(place_geojson.properties, data);
        $('#saveNotification').text("Saving...");
        var json = JSON.stringify(place_geojson);
        
        var $xhr = $.ajax({
            'url': API_URL,
            'data': json,
            'type': 'POST',
            'dataType': 'json'
        })
        .success(function(response) {
                $('#saveNotification').text("Saved");
                window.location.href = $G.placeUrlPrefix  + response.properties.id
        })
        .fail(function(response) {
            alert("error saving");
            $('#saveNotification').text(response.error);
        });     
    });  
});
