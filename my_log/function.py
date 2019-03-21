def singleton(klass):
    """
    singleton function
    :param klass: instance of class
    :return: object is create or object is exits
    """
    if not klass._instance:
        klass._instance = klass()
    return klass._instance
