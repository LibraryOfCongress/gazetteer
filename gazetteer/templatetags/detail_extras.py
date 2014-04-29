from django import template
register = template.Library()

@register.filter
def lower(value): 
    """Converts a string into all lowercase"""
    return value.lower()
    
@register.filter
def to_admin_string(admin_list):
    
    admin_names = ""
    if len(admin_list) > 0:
        name_array = ["","","","","", ""]
        for admin in admin_list:
            if admin["feature_code"] == "ADMO":
                name_array[0] = name_array[0] + " " + admin["name"]
            elif admin["feature_code"] == "ADM1":
                name_array[1] = name_array[1] + " " + admin["name"]
            elif admin["feature_code"] == "ADM2":
                name_array[2] = name_array[2] + " " + admin["name"]
            elif admin["feature_code"] == "ADM3":
                name_array[3] = name_array[3] + " " + admin["name"]
            elif admin["feature_code"] == "ADM4":
                name_array[4] = name_array[4] + " " + admin["name"]
            else:
                name_array[5] = name_array[5] + " " + admin["name"]
        print name_array
        
        name_array_clean = []
        for admin_name in name_array:
            if admin_name:
                name_array_clean.append(admin_name)
        admin_names = (",").join(name_array_clean)

    return admin_names
