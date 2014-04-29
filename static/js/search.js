//'use strict';

(function($) {

var map, jsonLayer;

$(window).load(function() {
    $('.mapListSection').css({'opacity': 0});
    $('#jsonLink').hide();

    var osm = new L.TileLayer($G.osmUrl,{minZoom:1,maxZoom:18,attribution:$G.osmAttrib});
    map = new L.Map('map', {layers: [osm], center: new L.LatLng($G.centerLat, $G.centerLon), zoom: $G.defaultZoom });
    
    //update search when map viewport changes
    map.on("moveend", function(e) {
        var center = map.getCenter();
        var zoom = map.getZoom();
        var urlData = queryStringToJSON(location.search);

        //this line is because moveend gets triggered when map is moved due to onpopstate(), in which case we don't want to call search again     
        if (urlData.lat == center.lat && urlData.lon == center.lng && urlData.zoom == center.zoom) {
            return;
        }

        //actually do the search in 250ms if user has not moved map any further                
        setTimeout(function() {
            var newCenter = map.getCenter()
            var newZoom = map.getZoom()
            if (center.lat == newCenter.lat && center.lng == newCenter.lng && zoom == newZoom) {
                submitSearch({
                    'bboxChanged': true
                });
            }
        }, 250);

    });
    

    //Define JSON layer
    jsonLayer = L.geoJson(null, {
        onEachFeature: function(feature, layer) {
            feature.properties.highlighted = false;
            var id = feature.properties.id;
            layer.bindPopup(getPopupHTML(layer.feature.properties));

            layer.on("mouseover", function(e) {
                layer.feature.properties.highlighted = true;
                jsonLayer.setStyle(styleFunc);                
                //map.closePopup();
                var $row = $('#feature' + id);
                $row.addClass("highlighted");
            });
            layer.on("mouseout", function(e) {
                layer.feature.properties.highlighted = false;
                jsonLayer.setStyle(styleFunc);
                var $row = $('#feature' + id);
                $row.removeClass("highlighted");            
            });

            layer.setStyle($G.styles.geojsonDefaultCSS);
        },
        pointToLayer: function(feature, latlng) {
            //Convert point fields to circle markers to display on map
            return L.circleMarker(latlng, $G.styles.geojsonDefaultCSS);
        }

    }).addTo(map);

    function getPopupHTML(props) {
        var $container = $("<div />").addClass("popupContainer");
        var $title = $("<h3 />").text(props.name).appendTo($container);
        var admin_names = toAdminString(props)
        $("<span class='admin_names'>"+admin_names+"</span>").appendTo($container)
        var $type = $('<div />').html("<strong>Type:</strong> " + props.feature_code_name).appendTo($container);
        if (props.timeframe.hasOwnProperty("start")) {
            var $timeframe = $('<div />')
                .html("<strong>Timeframe:</strong> " + props.timeframe.start + " to " + props.timeframe.end)
                .appendTo($container);
        }
        var $uriList = $('<div />').html("<strong>URIs:</strong> ").appendTo($container);
        var $uriUl = $('<ul />').appendTo($uriList);
        $.each(props.uris, function(i, v) {
            //console.log(i, v);
            var $uriLi = $('<li />').appendTo($uriUl);
            if (v.length > 40) {
                var uriString = v.substr(0,40) + "...";
            } else {
                var uriString = v;
            }
           
            var $uriA = $('<a />').attr("target", "_blank").attr("href", v).text(uriString).appendTo($uriLi);
        });

        var placeUrl = $G.placeUrlPrefix + props.id;
        var $placeLinkP = $('<p />').appendTo($container);
        var $placeLink = $('<a />').attr("href", placeUrl).text("View / Edit").appendTo($placeLinkP);
        return $container.html();        
    }

    /*
    Function to submit search and display results
    Accepts options:
        pushState: if true (default), also push URL state.  
    */
    function submitSearch(options) {
        var o = $.extend({
            //'bboxChanged': false,
            'pushState': true                
        }, options);
            
        var currentState = queryStringToJSON(location.search);
        var search_term = $('#searchField').val();

        if ($.trim(search_term) === '') return; //if search term is empty, do nothing, return. FIXME: user may want to search for empty string
        var geo = $('input[name=geo]:checked').val() == 'no_geo' ? false : true;
        //console.log(geo);

        if (geo) {
            var center = map.getCenter()
            var zoom = map.getZoom()
            currentBounds = map.getBounds() // .toBBoxString();
            var bbox = toBBoxString(currentBounds);
        } else {
            var bbox = "false"; //send "false" as string to backend
        }

        //console.log(bbox);        
        //if search term has changed from what's in the URL, set page no to 1
        if (currentState.hasOwnProperty("q")) {
            if (decodeURIComponent(currentState.q) != search_term) {
                $('#page_no').val('1');
            }                    
        }

        //Get page no
        var page_no = parseInt($('#page_no').val());        
        var totalPages = parseInt($('#totalPages').text());

        var start_date = $.trim($('#startDate').val !== '') ? $('#startDate').val() : false; 
        var end_date = $.trim($('#endDate').val !== '') ? $('#endDate').val() : false; 


        if (totalPages === 0) {
            page_no = 1;
        } else if (page_no > totalPages) {
            page_no = totalPages;
        }


        //Set 'loading' states        
        jsonLayer.clearLayers();
        $('#searchField').addClass("loading");
        $('#searchTerm').text(search_term);
        $('#searchField').attr("disabled", "disabled");
        $('#searchButton').attr("disabled", "disabled");
        $('#mapList tbody').empty();
        $('#currPageNo').text('*');
        
        //get URL to use for pushState
        var timeframeParams = '';
        if (start_date) {
            timeframeParams += '&start_date=' + start_date;
        }

        if (end_date) {
            timeframeParams += '&end_date=' + end_date;
        }

        var feature_type = $('#featureCodeFilter').val();
        if (feature_type) {
            var ftParams = '&feature_type=' + feature_type;
        } else {
            var ftParams = '';
        }

        var urlParams = "?" + 'q=' + encodeURIComponent(search_term) + ftParams + '&page=' + page_no + timeframeParams;
        if (geo) {
            urlParams += '&lat=' + center.lat + '&lon=' + center.lng + '&zoom=' + zoom;
        } else {
            urlParams += "&bbox=false"; //FIXME
        }


        if (o.pushState) {
            //console.log("pushing state " + urlParams);
            history.pushState({}, "Gazetteer Search: " + search_term, urlParams);
        }
        document.title = "Gazetteer Search: " + search_term

        //FIXME: rationalize URLs ?
        //Get URL to use for GeoJSON feed
        var searchParams = {
            'q': encodeURIComponent(search_term),
            'bbox': bbox,
            'page': page_no
        }
        
        if (start_date) {
            searchParams.start_date = start_date;
        }
        
        if (end_date) {
            searchParams.end_date = end_date;
        }

        
        if (feature_type != '') {
            searchParams.feature_type = feature_type;
        }
        //console.log(searchParams);

        var geojsonUrl = JSONtoQueryString(searchParams);       
        var feedUrl = $G.apiBase + "search.json" + geojsonUrl;
        $('#jsonLink').attr("href", feedUrl); 

        $.getJSON($G.apiBase + "search.json" + geojsonUrl, function(features) {

            //If search results area is hidden, show
            if ($('.mapListSection').css("opacity") == '0') {
                $('.mapListSection').animate({'opacity': '1'}, 1000);
                $('#jsonLink').show();
                
            }

            //If the server sent an 'error' property, alert it and return
            //FIXME: better handling of errors
            if (features.hasOwnProperty("error") && features.error != '') {
                alert(features.error);
                return;
            }
            
            //populate pagination details
            $('#noOfResults').text(features.total);
            $('#currPageNo').text(features.page);
            $('#totalPages').text(features.pages);
            if (features.total === 0) {
                $('#currPageNo').text('0');
                $('#totalPages').text('0');                
            }
            $('#searchField').removeAttr("disabled");
            $('#searchField').removeClass("loading");
            $('#searchButton').removeAttr("disabled");

            //Add features to map if results are geo
            if (geo) {
                jsonLayer.addData(features);
            }

            //add features to results table
            for (var i=0; i<features.features.length;i++) {
                var f = features.features[i];
                var props = f.properties;
                var listItem = getRow(props);
                $('#mapList tbody').append(listItem);
            }
                   
        });
    }

    //When search form is submitted, eg. by user pressing 'enter' in search field
    $('#searchForm').submit(function(e) {
        e.preventDefault();
        submitSearch();
    });    

    //Handle URL / window onpopstate
    window.onpopstate = function(obj) {
        var queryString = location.search;
        var data = queryStringToJSON(queryString);

        if (data.q) {
            $('#searchField').val(decodeURIComponent(data.q));
        }
        if (data.page) {
            $('#page_no').val(data.page);
        }

        //FIXME: better error handling for invalid values
        if (data.lat && data.lon) {
            $('#geo_radio').attr("checked", "checked");
            if (!data.zoom) {
                data.zoom = 5; //if lat and lng exist, but zoom is missing, set to value of 5 (is this sane?)
            }
            map.setView([data.lat, data.lon], data.zoom);
        }

        if (data.bbox == "false") {
            $('#no_geo_radio').attr("checked", "checked");
        }

        if (data.start_date) {
            $('#startDate').val(data.start_date);
        }

        
        if (data.feature_type) {
            $('#featureCodeFilter').val(data.feature_type);
        }

        if (data.end_date) {
            $('#endDate').val(data.end_date);
        }

        submitSearch({
            'pushState': false
        });
    };

    //call window.onpopstate() on page load.
    window.onpopstate();


    /* pagination code */
    $('.first').click(function() {
        $('#page_no').val('1');
        $('#searchForm').submit();
    });

    $('.last').click(function() {
        var lastPage = parseInt($('#totalPages').text());
        $('#page_no').val(lastPage);
        $('#searchForm').submit();
    });

    $('.next').click(function() {
        var currPage = parseInt($('#page_no').val());
        var lastPage = parseInt($('#totalPages').text());
        if (currPage < lastPage) {
            $('#page_no').val(currPage + 1);
            $('#searchForm').submit();
        }
    });

    $('.previous').click(function() {
        var currPage = parseInt($('#page_no').val());
        if (currPage > 1) {
            $('#page_no').val(currPage - 1);
            $('#searchForm').submit();            
        }
    });
    /* pagination code end */

    //silly code to set the size of the table to fit in the viewport
    $(window).resize(function() {
        var $tbody = $('#mapList tbody');
        var topOffset = $tbody.offset().top;
        var footerHeight = $('#footer').height();
        var viewportHeight = $(window).height();
        var resultsBlockHeight = $('#resultsBlock').height();
        $tbody.height(viewportHeight - (topOffset + footerHeight + resultsBlockHeight));
    });
    $(window).resize();

});


//function to return a jQuery DOM element for each feature row.
function getRow(props) {
    var $tr = $('<tr />').attr("id", "feature" + props.id).data("id", props.id).data("properties", props).hover(function() {
        var id = $(this).attr("id");
        id = id.replace("feature", "");
        var layer = getFeatureById(id);
        layer.feature.properties.highlighted = true;
        jsonLayer.setStyle(styleFunc);
        layer.bringToFront();
    }, function() {
        var id = $(this).attr("id");
        id = id.replace("feature", "");
        var layer = getFeatureById(id);
        layer.feature.properties.highlighted = false;
        jsonLayer.setStyle(styleFunc);            
    });
    var $one = $('<td />').addClass("col1").appendTo($tr);
    var $a = $('<a />').attr("href", $G.placeUrlPrefix + props.id).text(props.name).appendTo($one);
    

    var admin_names = toAdminString(props)
    $("<br /><span class='admin_names'>"+admin_names+"</span>").appendTo($one)

    $('<td />').addClass("col2").text(props.feature_code + ": " + props.feature_code_name).appendTo($tr);


    if (props.hasOwnProperty("timeframe") && props.timeframe != null && props.timeframe.hasOwnProperty("start")) {
        var timeframeTxt = props.timeframe.start + " to " + props.timeframe.end;
    } else {
        var timeframeTxt = "-";
    }
    $('<td />').addClass("col3").text(timeframeTxt).appendTo($tr);

    //get "origin", from first uri, set on HTML element, and then access "hostname" property to show only the hostname
    var $originTd = $('<td />').addClass("col4").appendTo($tr);    
    if (props.uris[0] && $.trim(props.uris[0] !== '')) {
        var $originElem = $('<a />')
            .attr("href", props.uris[0])
            .attr("_target", "blank")
            .appendTo($originTd);
        var hostname = $originElem.get(0).hostname;
        $originElem.text(hostname);
    }

    return $tr;     
}


//get feature on map based on feature id
function getFeatureById(feature_id) {
    var ret = false;
    jsonLayer.eachLayer(function(layer) {
        if (layer.feature.properties.id == feature_id) {
            ret = layer;
        }
    });
    return ret;
}


//set styles for highlighted layer on map
function styleFunc(feature) {
    switch (feature.properties.highlighted) {
        case true:
            return $G.styles.geojsonHighlightedCSS;
        case false:
            return $G.styles.geojsonDefaultCSS;
    } 
}

//FIXME: move following utility functions somewhere, perhaps gazetteer.js
/*
Convert a JSON object to a URL query string
>>>var foo = {'var1': 'bar', 'var2': 'baz'}
>>> JSONtoQueryString(foo);
'?var1=bar&var2=baz'
*/
function JSONtoQueryString(obj) {
    var s = "?";
    for (var o in obj) {
        if (obj.hasOwnProperty(o)) {
            s += o + "=" + obj[o] + "&";
        }
    }
    return s.substring(0, s.length - 1);
}

/*
Convert a URL query string to a JSON object
>>>var foo = "/something/bla/?var1=bar&var2=baz";
>>>QueryStringToJSON(foo);
{'var1': 'bar', 'var2': 'baz'}
*/
function queryStringToJSON(qstring) {
    if (qstring.indexOf("?") == -1) {
        return {};
    }
    var q = qstring.split("?")[1];
    var args = {};
    var vars = q.split('&');
//    console.log(vars);
    for (var i=0; i<vars.length; i++) {
        var kv = vars[i].split('=');
        var key = kv[0];
        var value = kv[1];
        args[key] = value;
    }		
    return args;		
}


/*
    Returns sane bbox values from a Leaflet bounds object - normalizes values over 180 / 90 on either side.
*/
function toBBoxString(leafletBounds) {
    var s = leafletBounds.toBBoxString();
    var arr = s.split(",");
    arr[0] = parseFloat(arr[0]) <= -180 ? '-179.99' : arr[0];
    arr[1] = parseFloat(arr[1]) <= -90 ? '-89.99' : arr[1];
    arr[2] = parseFloat(arr[2]) >= 180 ? '179.99' : arr[2];
    arr[3] = parseFloat(arr[3]) >= 90 ? '89.99' : arr[3];
    return arr.join(",");
}

/*
>>>bboxFromString('-1,2,-5,6')
>>>[[2,-1],[6,-5]]

function bboxFromString(s) {
    var points = s.split(",");
    var southwest = new L.LatLng(points[1], points[0]);
    var northeast = new L.LatLng(points[3], points[2]);
    return [southwest, northeast]
}
*/



})(jQuery);

