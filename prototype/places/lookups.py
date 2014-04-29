from places.models import FeatureType
from django.db.models import Q

class FeatureTypeLookup(object):

    def get_query(self,q,request):
        """ return a query set.  you also have access to request.user if needed """
        return FeatureType.objects.filter(Q(code__icontains=q) | Q(name__icontains=q))

    def format_result(self,ftype):
        """ the search results display in the dropdown menu.  may contain html and multiple-lines. will remove any |  """
        return u"%s: %s" % (ftype.code, ftype.name,)

    def format_item(self,ftype):
        """ the display of a currently selected object in the area below the search box. html is OK """
        return unicode(ftype)

    def get_objects(self,ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
            this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        return FeatureType.objects.filter(pk__in=ids).order_by('code')
