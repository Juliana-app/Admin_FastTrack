def es_admin_processor(request):
    if request.user.is_authenticated:
        return {'es_administrador': request.user.rol == 'administrador'}
    return {'es_administrador': False}
