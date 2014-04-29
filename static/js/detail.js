'use strict';

var map, jsonLayer, similarPlacesLayer;

$(function() {
    
//    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
//    var osmAttrib='Map data © openstreetmap contributors';
    var osm = new L.TileLayer($G.osmUrl,{minZoom:1,maxZoom:18,attribution:$G.osmAttrib});
    map = new L.Map('map', {
        layers: [osm],
        center: new L.LatLng($G.centerLat, $G.centerLon),
        zoom: $G.defaultZoom,
        crs: L.CRS.EPSG900913 
    });
    
        
    if (!isEmptyPlace(place_geojson.geometry)) {
        var place_has_geo = true;
        jsonLayer = L.geoJson(place_geojson, {
            'pointToLayer': function(feature, latlng) {
                return L.circleMarker(latlng, $G.styles.geojsonHighlightedCSS);
            }
        }).addTo(map);
        var bounds = jsonLayer.getBounds();
        map.fitBounds(bounds);
    } else {
        var place_has_geo = false;
    }


    if (wms_layers.length > 0) {
        var mapWMSLayers = {};
        wms_layers.forEach(function(layer, i) {
            mapWMSLayers[layer] = L.tileLayer.wms(layer, {'format': 'image/png'}).addTo(map).bringToFront();
        });
        var layersControl = L.control.layers({}, mapWMSLayers, {
            'position': 'bottomleft',
            'collapsed': true
        }).addTo(map);    
    }


    //filter out similar places with no geometries to send valid geojson to Leaflet
    var cleaned_features = $.map(similar_geojson.features, function(v, i) {
        if ($.isEmptyObject(v.geometry)) {
            return null;
        } else {
            return v;
        }
    });
    var cleaned_similar_geojson = $.extend(true, {}, similar_geojson);
    cleaned_similar_geojson.features = cleaned_features;    

    similarPlacesLayer = L.geoJson(cleaned_similar_geojson, {
        'onEachFeature': function(feature, layer) {
            feature.properties.highlighted = false;
            var id = feature.properties.id;
            var selector = '.similarPlace[data-id=' + id + ']';
            layer.on("mouseover", function(e) {
                $(selector).addClass("highlighted");
            });
            layer.on("mouseout", function(e) {
                $(selector).removeClass("highlighted");
            });
            layer.on("click", function(e) {
                var url = feature_url_prefix + feature.properties.id;
                location.href = url;
            });
        },
        'pointToLayer': function(feature, latlng) {
            return L.circleMarker(latlng, $G.styles.similarPlacesDefaultCSS);
        }        

    });

    $('.similarPlace').hover(function() {
        var $this = $(this);
        var id = $this.attr("data-id");
        //console.log(id);
        var layer = getFeatureById(id, similarPlacesLayer);
        //console.log(layer);
        if (layer) {
            layer.feature.properties.highlighted = true;
            layer.bringToFront();
            similarPlacesLayer.setStyle(styleFunc);
        }
    }, function() {
        var $this = $(this);
        var id = $this.attr("data-id");
        var layer = getFeatureById(id, similarPlacesLayer);
        if (layer) {
            layer.feature.properties.highlighted = false;
            similarPlacesLayer.setStyle(styleFunc);
        }    
    });

    $('.rollback_place').click(function(e) {
        e.preventDefault();
        var revision_id = $(this).attr("data-revision");
        var url = $G.apiBase + place_geojson.properties.id + "/" + revision_id + ".json";
        var comment = prompt("Please add a comment / note about this change.");
        var data = {
            'comment': comment
        }
        var $xhr = $.ajax({
            'url': url,
            'data': JSON.stringify(data),
            'type': 'PUT',
            'dataType': 'json'
        }).success(function(data) {
            window.location.reload();
            //console.log(data);
        });
    });

    $('#searchPlaceButton').click(function(e){
        var geojsonUrl = "?per_page=10&q="+$("#searchPlace").val()

        e.preventDefault();
        $('#similarPlaces').slideDown();
        $('ul#similarPlaces .blankSimilarPlace').remove()
        $('ul#similarPlaces hr').remove()
        
        $.getJSON($G.apiBase + "search.json" + geojsonUrl, function(features) {
            $("#similarPlaces").prepend("<hr  />")
            for (var i=0; i<features.features.length;i++) {
                var f = features.features[i];
                var props = f.properties;
                var place = $("ul#searchedPlaces .blankSimilarPlace").clone()  //with data and events?
                place.attr("style", "")
                place.attr("data-id", props.id)
                var similarPlaceA = $(".similarPlaceA", place)
                var simhref = similarPlaceA.attr("href")
                
                similarPlaceA.attr("href", simhref.slice(0, -1) + props.id)
                var admin_names = toAdminString(props)
                var admin_span =  $(".admin_names", place)
                admin_span.html(admin_names)
                similarPlaceA.html(props.name)
                $("#similarPlaces").prepend(place)
            }
            
            
            });
        });

    $('#showSimilar').toggle(function(e) {
        e.preventDefault();
        $(this).text("Hide Similar");
        $('#similarPlaces').slideDown();
        similarPlacesLayer.addTo(map).bringToBack();
        var bounds = similarPlacesLayer.getBounds();
        map.fitBounds(bounds);
    }, function(e) {
        e.preventDefault();
        $(this).text("Show Similar");
        $('#similarPlaces').slideUp();
        map.removeLayer(similarPlacesLayer);
        if (place_has_geo) {
            var bounds = jsonLayer.getBounds();
            map.fitBounds(bounds);
        }
    });

    $('#similarPlaces').delegate(".addRelation", "click", function(e) {
        e.preventDefault();
        var $li = $(this).closest("li");
        var id1 = place_geojson.properties.id;
        var id2 = $li.attr("data-id");
        var id2_url = $li.find(".similarPlaceA").attr("href");
        var id2_name = $li.find(".similarPlaceA").text();
        var relation = $li.find(".relation_type").val();
        if (relation === '') {
            alert("please add a relation first");
            return;
        }
        var comment = prompt("Please add a comment for this change");
        var url = "/1.0/place/" + id1 + "/" + relation + "/" + id2 + ".json";
        var $xhr = $.ajax({
            'url': url,
            'data': JSON.stringify({'comment': comment}),
            'type': 'PUT',
            'dataType': 'json'
        });
        $xhr.success(function(response) {
            var $tr = $('<tr />').attr("data-id", id2);
            var $td1 = $('<td />').appendTo($tr);
            var $a = $('<a />').attr("href", id2_url).text(id2_name).appendTo($td1);
            var $td2 = $('<td />').addClass("relation").text(relation).appendTo($tr);
            var $td3 = $('<td />').addClass("deleteRelation").text("X").appendTo($tr);
            $('#relationsTable tbody').append($tr); 
        });
        $xhr.fail(function(err) {
            alert("adding relation failed");
        });
    });
    $('#relationsTable').delegate(".deleteRelation", "click", function(e) {

        e.preventDefault();
        var $tr = $(this).closest("tr");
        var id1 = place_geojson.properties.id;
        var id2 = $tr.attr("data-id");
        var relation = $.trim($tr.find(".relation").text());
        var url = "/1.0/place/" + id1 + "/" + relation + "/" + id2 + ".json";
        var comment = prompt("Please add a comment for this change");
        var $xhr = $.ajax({
            'url': url,
            'data': {'comment': comment},
            'type': 'DELETE',
            'dataType': 'json'
        });
        $xhr.success(function(response) {
            $tr.slideUp().remove();
        });
        $xhr.fail(function(err) {
            alert("failed at deleting relation");
        });
    });

    $('#showHistory').toggle(function(e) {
        e.preventDefault();
        $(this).text("Hide History");
        $('#revisions').slideDown();
    }, function(e) {
        e.preventDefault();
        $(this).text("Show History");
        $('#revisions').slideUp();
    });

    $('#showAlternateNames').click(function(e) {
        e.preventDefault();
        $('#alternateNamesTable').toggle();
    });

    $('.collapseChild').click(function() {
        $(this).parent().find('ul').toggle();
    });

    $('.toggleNext').click(function(e) {
        e.preventDefault();
        $(this).next().toggle();
    });

    $('#uriList a').each(function() {
        $(this).attr("target", "_blank");
    });

    $('#addAlternateName').click(function(e) {
        e.preventDefault();
        var $tr = $('#alternateNamesTable tbody tr').eq(0).clone();
        $tr.find('input').val('');
        $('#alternateNamesTable tbody').append($tr.show());
    });

    $('.removeAltName').click(function() {
        $(this).closest('tr').remove();
    });

    //handle ajax-ifying edit / save
    //FIXME: this needs to be architected very differently
    var SAVE_URL = $G.apiBase + place_geojson.properties.id + ".json";
    //var SAVE_URL = "/1.0/place/" + place_geojson.properties.id + ".json";
    $('#editPlace').toggle(function(e) {
        e.preventDefault();
        $(this).text("Save");
        $('.commitMessage').show();
        //handle place name input
        var $placeName = $('#placeName');
        var currentPlaceName = $.trim($placeName.text());
        $placeName.data("oldVal", currentPlaceName);
        $placeName.empty();
        var $placeNameInput = $('<input />')
            .attr("id", "placeNameInput")
            .val(currentPlaceName)
            .appendTo($placeName);

        //make alternate names editable
        $('#alternateNamesTable input[disabled]').removeAttr("disabled");
        $('#timeframes *[disabled]').removeAttr("disabled");
        $('.removeAltName').show();
        $('#alternateNamesTable tfoot').show();

        //handle feature code input with select2 autocomplete
        var featureCode = place_geojson.properties.feature_code;
        var featureCodeName = place_geojson.properties.feature_code_name;
        //console.log(featureCode);
        var $featureCode = $('#featureCode').empty();         
        var $featureCodeInput = $('<input />')
            .attr("id", "featureCodeInput")
            .val(featureCode)
            .width(300)
            .appendTo($featureCode);
            
        $featureCodeInput.select2({
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
                place_geojson.properties.feature_code_name = item.name; //FIXME: please look through select2 docs and move to an onSelect type callback, but this works for now.
                return item.typ + ": " + item.name;           
                //return "<div data-id='" + item.id + "'>" + item.first_name + " " + item.last_name + "</div>";
            },
            initSelection: function(elem, callback) {
                var val = $(elem).val();
                var data = {
                    'id': val,
                    'typ': val,
                    'name': featureCodeName
                };
                callback(data); 
            }
        });
                    
    }, function(e) {
        e.preventDefault();
        var $btn = $(this);
        $btn.hide();
        $('#saveStatus').text("Saving...");
        place_geojson.properties.feature_code = $('#featureCodeInput').val();        
        place_geojson.properties.name = $('#placeNameInput').val();
        place_geojson.comment = $('#comment').val();

        // get alternate names from input elements, perhaps re-factor into separate function
        var alternate_names = [];
        $('#alternateNamesTable tbody tr:visible').each(function() {
            var $this = $(this);
            alternate_names.push({
                'lang': $this.find('.alternateLang').val(),
                'name': $this.find('.alternateName').val(),
                'type': $this.find('.alternateType').val()
            });
        });
        place_geojson.properties.alternate = alternate_names;

        //handle getting / saving time-frame data FIXME: validations
        if ($('#timeframe_start').val() != '') {
            var timeframe = {
                'start': $('#timeframe_start').val(),
                'start_range': $('#timeframe_start_range').val(),
                'end': $('#timeframe_end').val(),
                'end_range': $('#timeframe_end_range').val()
            }
            place_geojson.properties.timeframe = timeframe;
        }

        var $xhr = $.ajax({
            'url': SAVE_URL,
            'data': JSON.stringify(place_geojson),
            'type': 'PUT',
            'dataType': 'json'
        })
        .success(function(response) {
                //console.log(response);
                location.reload();
//                place_geojson = response;
//                $('#saveStatus').hide();
//                $btn.text("Edit").show();
//                $('#placeName').empty().text(place_geojson.properties.name);
//                $('#featureCodeInput').select2("destroy").remove();
//                var featureCodeString = place_geojson.properties.feature_code + ": " + place_geojson.properties.feature_code_name;
//                $('#featureCode').empty().text(featureCodeString);
                //TODO: in an ideal world, read the revisions JSON and update History.                
        })
        .fail(function(response) {
            alert("error saving");
            $('#saveStatus').text(response.error);
        });      

    });
    //END handle ajax edit /save.

    $('.tabButtons li a').click(function(e) {
        //e.preventDefault();
        var $this = $(this);
        if ($this.hasClass("selectedTab")) {
            return;
        }
        if ($('.selectedTab').length > 0) {
            var displayedTab = $('.selectedTab').attr("href");
            $('.selectedTab').removeClass("selectedTab");
            $(displayedTab).hide();
        }

        $this.addClass("selectedTab");
        var idToDisplay = $this.attr("href");
        //console.log(idToDisplay);
        $(idToDisplay).show();

    });

    //if location.hash exists, click on tab button with that href
    if (location.hash != '') {
        $('a[href=' + location.hash + ']').click();
    }
    

});


function styleFunc(feature) {
    switch (feature.properties.highlighted) {
        case true:
            return $G.styles.similarPlacesHighlightedCSS;
        case false:
            return $G.styles.similarPlacesDefaultCSS;
    } 
}


//test if geometry is either undefined, null or empty object
function isEmptyPlace(geometry) {
    if (!geometry) return true;
    if ($.isEmptyObject(geometry)) return true;
    var coords = geometry.coordinates;
    if (geometry.type == "Point" && coords.length < 2) return true;
//    if (parseFloat(coords[0]) > 0 && parseFloat(coords[0]) < 1 && parseFloat(coords[1]) > 0 && parseFloat(coords[1]) < 1) return true;
    return false;
}

function getFeatureById(feature_id, layer) {
    //var ret = false;
    //console.log("Feature_id", feature_id);
    //var id = feature_id.replace("feature", "");
    var ret = false;
    layer.eachLayer(function(layer) {
        if (layer.feature.properties.id == feature_id) {
            ret = layer;
        }
    });
    return ret;
}

