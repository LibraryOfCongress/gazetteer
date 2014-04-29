from django.forms.models import modelformset_factory
from django.forms.models import BaseModelFormSet
from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField

from models import Relationship

# create a superclass
class BaseRelationsFormSet(BaseModelFormSet):

    # that adds the field in, overwriting the previous default field
    def add_fields(self, form, index):
        super(BaseRelationsFormSet, self).add_fields(form, index)
        form.fields["feature2"] = AutoCompleteSelectField('feature', required=False)

# pass in the base formset class to the factory
# RelationFormSet = modelformset_factory(Relationship,fields=('feature2','relationship_type'),extra=1,formset=BaseRelationsFormSet)
