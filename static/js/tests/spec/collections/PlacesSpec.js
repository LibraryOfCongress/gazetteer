
describe("testing places", function() {
    
    var done = false,
        that = this;
    beforeEach(function() {
        require(['app/collections/places'], function(Places) {
            that.places = new Places();
            that.places.fetch();
            that.places.on("reset", function() {
                done = true;
            });
        });
        waitsFor(function() {
            return done;
        });
    });

    
    it("should fetch 100 places", function() {
        expect(that.places.length).toEqual(100);
    });

    it("should set Server API options", function() {

        that.places.setServerApi({
            'q': 'testSearch',
            'start_date': '1900',
            'end_date': '2000'
        });
        expect(that.places.server_api.q).toEqual('testSearch');
        expect(that.places.server_api.start_date).toEqual('1900');
        expect(that.places.server_api.end_date).toEqual('2000');
    
    });

});


