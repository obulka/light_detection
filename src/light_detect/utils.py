"""Utility Functions."""


def autoset_property(property_method):
    """Wraps a class property to automatically set the corresponding
    instance variable if it evaluates False. This requires the instance
    variable name be an underscore followed by the property method name,
    and a corresponding setter method be implemented and named _set
    followed by the instance variable name. This allows automatic
    caching of potentially slow to set variables.

    Args:
        property_method (method):
            The class property that is to be decorated.
    """
    @property
    def decorated(self):
        """Decorate the property method with the ability to
        automatically set the corresponding instance variable of the
        class.
        """
        property_method_name = property_method.__name__
        internal_property = getattr(self, f"_{property_method_name}")

        if not internal_property:
            getattr(self, f"_set_{property_method_name}")()
        return property_method(self)

    return decorated
