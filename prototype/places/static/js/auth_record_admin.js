$(function() {
    $.getJSON("/auth_record.json", {
        'id': RECORD_ID
    }, function(features) {
        for (var i=0; i<features.features.length;i++) {
            var f = features.features[i];
            var props = f.properties;
            var listItem = getRow(props);
            $('#mapList tbody').append(listItem);
        }                  
    });

});



/*
function copied over from gazetteer.js. TODO:resolve to DRY.
*/
function getRow(props) {
    var $tr = $('<tr />');
    var $one = $('<td />').appendTo($tr);
    var $a = $('<a />').attr("href", "/admin/places/feature/" + props.id).text(props.preferred_name).appendTo($one);
    $('<td />').text(props.uri).appendTo($tr);
    $('<td />').text(props.feature_type).appendTo($tr);
    $('<td />').text(props.admin2).appendTo($tr);
    $('<td />').text(props.admin1).appendTo($tr);
    return $tr;     
}

