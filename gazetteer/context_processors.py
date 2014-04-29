import settings

def gazetteer_params(request):
    return {'GAZETTEER': settings.GAZETTEER}
