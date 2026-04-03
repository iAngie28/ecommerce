def get_auth_extra_data(user):
    """
    Obtiene la información adicional necesaria tras un login exitoso.
    """
    extra_data = {
        'user_name': user.username,
        'subdomain': None
    }
    
    if user.tenant:
        # Aquí movemos la lógica de filtrado que tenías en el serializer
        domain_obj = user.tenant.domains.filter(is_primary=True).first()
        extra_data['subdomain'] = domain_obj.domain if domain_obj else None
        
    return extra_data