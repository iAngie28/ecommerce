def get_auth_extra_data(user):
    """
    Obtiene la información adicional necesaria tras un login exitoso.
    """
    extra_data = {
        'user_name': user.email,
        'full_name': user.get_full_name() or user.email.split('@')[0].capitalize(),
        'tenant_id': None,
        'schema_name': None,
        'subdomain': None
    }
    
    if user.tenant:
        extra_data['tenant_id'] = user.tenant.id
        extra_data['schema_name'] = user.tenant.schema_name
        
        # Obtener el dominio primario del tenant
        domain_obj = user.tenant.domains.filter(is_primary=True).first()
        if domain_obj:
            extra_data['subdomain'] = domain_obj.domain
        else:
            extra_data['subdomain'] = f"{user.tenant.schema_name}.localhost"
        
    return extra_data