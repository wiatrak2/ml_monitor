def safe_init(variable, instance):
    if variable is None:
        return instance
    return variable
