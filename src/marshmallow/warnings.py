class RemovedInMarshmallow4Warning(DeprecationWarning):
    """
    Warning class to indicate functionality that will be removed in Marshmallow 4.

    This warning is a subclass of DeprecationWarning and is used to notify users
    about features or behaviors that are deprecated and will be removed in the
    next major version (Marshmallow 4) of the library.
    """

    def __init__(self, message):
        super().__init__(message)
