$(function() {
    $.getJSON("/feature/" + FEATURE_ID + "/similar.json", {
        
    }, function(data) {
        if (data.length > 12) {
            var counter = 12;
        } else {
            var counter = data.length;
        }
        for (var i=0; i<counter; i++) {
            var $row = getRow(data[i]);
            $('#similarTable tbody').append($row);
        }
    });
});

var RELATIONSHIP_OPTIONS = ['conflates', 'contains', 'replaces', 'supplants']

function getRow(d) {
    var $tr = $('<tr />').data("id", d.id);
    var $one = $('<td />').appendTo($tr);
    var $a = $('<a />').attr("href", "/admin/places/feature/" + d.id).text(d.preferred_name).appendTo($one);
    var similarity = Math.round(parseFloat(d.similarity) * 1000) / 10;
    var distance = Math.round(parseFloat(d.distance));
    $('<td />').text(d.feature_type).appendTo($tr);
    $('<td />').text(similarity).appendTo($tr);
    $('<td />').text(distance).appendTo($tr);
    $('<td />').text(d.time_frame).appendTo($tr);
    var $primary_td = $('<td />').appendTo($tr);
    var $checkbox = $('<input />').attr("type", "checkbox").attr("disabled", "disabled").appendTo($primary_td);
    if (d.is_primary) {
        $checkbox.attr("checked", "checked");
    } else {
        $.noop();
    }

    var $relations_td = $('<td />').prependTo($tr);
    if (d.related_by != '') {
	var verb = d.related_by.replace(/e?s$/i, "");
	var related_by = "is " + verb + "ed by";
	var $relationselect = $('<a />').attr("href", "/admin/places/feature/" + d.id)
					.text(related_by).appendTo($relations_td);
    } else {
	var $relationselect = $('<select />').appendTo($relations_td);
	var $opt1 = $('<option />').val('').text('---').appendTo($relationselect);

	for (var i=0; i<RELATIONSHIP_OPTIONS.length; i++) {
	    var r = RELATIONSHIP_OPTIONS[i];
	    $('<option />').val(r).text(r).appendTo($relationselect);
	}

	if (d.relates_to != '') {
	    $relationselect.children().each(function() {
		if ($(this).val() == d.relates_to) {
		    $(this).attr("selected", "selected");
		}
	    });
	}
    }

    $relationselect.change(function() {
        var feature1 = FEATURE_ID;
        var feature2 = $(this).parents("tr").data("id");
        var relation = $(this).val();
        $.getJSON("/add_relation", {
            'feature1': feature1,
            'feature2': feature2,
            'relation': relation    
        }, function(response) {
            if (response.error) {
                alert(response.error);
            } else {
                alert(response.success);
            }
        });        
    });

    return $tr;
}


