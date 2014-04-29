define(['jquery', 'app/settings', 'select2'], function($, settings) {
    return {
        initSelect2: function($elem, model) {
            if (typeof(model) == 'undefined') {
                model = false;
            }
            $elem.select2({
                ajax: {
                    'url': settings.api_base + "place/feature_codes.json",
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
                    $elem.trigger("fcodeChanged", [{'typ': item.typ, 'name': item.name}]);
                    model &&  model.set("currentFeatureName", item.name); //FIXME: use above event to handle this in model saving, remove this line.
                    return item.typ + ": " + item.name;
                },
                initSelection: function(elem, callback) {
                    var val = $(elem).val();
                    var data = {
                        'id': val,
                        'typ': val,
                        'name': model ? model.get('properties.feature_code_name') : ''
                    };
                    console.log('autocomplete data', data);
                    callback(data);
                }
                
            });
            return $elem;
        },
        destroySelect2: function($elem) {
            $elem.select2("destroy");
        }

    }

});
