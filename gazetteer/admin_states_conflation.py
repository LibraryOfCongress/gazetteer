from django.core.management import setup_environ

import settings
import itertools
setup_environ(settings)

from gazetteer.models import FeatureCode
from gazetteer.models import AdminBoundary

from gazetteer.place import *

es_settings = settings.ELASTICSEARCH["default"]
conn = ElasticHistory(es_settings["HOST"], timeout=120)
index = es_settings["INDEX"]
doc_type = es_settings["DOC_TYPE"]


results = Place.objects.search("* uris:*census.gov* feature_code:ADM1")

tiger_states = results["places"]
problem_names = []

def add_relation_and_alternate_name(source_place, target_place):
    source_place.alternate = source_place.alternate + target_place.alternate
    source_place.add_relation(target_place, "conflates", {"user":"admin_conflate_script", "comment": "automated state conflation to favour tiger line states" })


for tiger_state in tiger_states:
    ne_results = Place.objects.search("name:"+tiger_state.name  + " uris:*naturalearthdata* feature_code:ADM1", bbox=[-177.01171, -31.65338, -8.26171, 73.87371])

    if ne_results["total"] <> 1:
        problem_names.append(tiger_state.name)
        continue
    ne_place = ne_results["places"][0]
    print "conflating", ne_place.name
    add_relation_and_alternate_name(tiger_state, ne_place)
   
   
    
for tiger_state in tiger_states:
    for prob_name in problem_names:
        if prob_name == tiger_state.name:
            if prob_name == "California":
                results = Place.objects.search("name:"+tiger_state.name  + " -baja uris:*naturalearthdata* feature_code:ADM1", bbox=[-177.01171, -31.65338, -8.26171, 73.87371])
                ne_place = results["places"][0]
                add_relation_and_alternate_name(tiger_state, ne_place)
                problem_names.remove(prob_name)
                
            if prob_name == "Virginia":
                results = Place.objects.search("name:"+tiger_state.name  + " -west uris:*naturalearthdata* feature_code:ADM1", bbox=[-177.01171, -31.65338, -8.26171, 73.87371])
                ne_place = results["places"][0]
                add_relation_and_alternate_name(tiger_state, ne_place)
                problem_names.remove(prob_name)
        
print "All done! Some were not conflated:", problem_names
