"""Useful object representation."""


class Circle:
    """Represent a circle."""

    def __init__(self, center, radius):
        """Initialize the circle.

        Args:
            center (tuple):
                The center position of the circle.
            radius (float or int): The radius of the circle.
        """
        self._center = center
        self._radius = radius

    def __repr__(self):
        """str: Printable representation of the circle."""
        return f"{{Center: {self._center}, Radius: {self._radius}}}"

    @classmethod
    def as_integers(cls, center, radius):
        """Initialize the circle using rounded, integer values.

        Args:
            center (tuple(float, float)):
                The center position of the circle.
            radius (float): The radius of the circle.

        Returns:
            instance: The class instance intialized with integers.
        """
        rounded_center = tuple(round(center_pos) for center_pos in center)
        return cls(rounded_center, round(radius))

    @property
    def center(self):
        """tuple: The center position of the circle."""
        return self._center

    @property
    def radius(self):
        """float or int: The radius of the circle."""
        return self._radius
