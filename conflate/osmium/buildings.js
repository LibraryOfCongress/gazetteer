/*
  run with: osmjs -2 -l sparsetable -j objects_2pass.js OSMFILE
*/

Osmium.Callbacks.node = function() {
  if(!this.tags["name"] && !this.tags["place_name"]) return;
  if (!this.tags.building) return;
  print(JSON.stringify({
    "geom": [this.geom.lon, this.geom.lat],
    "tags": this.tags, 
    "type":"node", 
    "id": this.id
    })
  )
}

Osmium.Callbacks.area = function() {
  if(!this.tags["name"] && !this.tags["place_name"]) return;
  if (!this.tags.building) return;
  print(JSON.stringify({
    "geom": this.geom.toWKT(),
    "tags": this.tags, 
    "type":"node", 
    "id": this.id
    })
  )
}
