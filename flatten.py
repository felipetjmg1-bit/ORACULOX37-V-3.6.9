"""Helper module for a simple speckle object tree flattening."""

from collections.abc import Iterable

try:
    from specklepy.objects import Base
except ImportError:
    class Base:
        """Fallback Base class if specklepy is not installed locally."""
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)


def flatten_base(base: Base) -> Iterable[Base]:
    """Flatten a base object into an iterable of bases.

    This function recursively traverses the `elements` or `@elements` attribute of the
    base object, yielding each nested base object.

    Args:
        base (Base): The base object to flatten.

    Yields:
        Base: Each nested base object in the hierarchy.
    """
    elements = getattr(base, "elements", getattr(base, "@elements", None))

    if elements is not None:
        for element in elements:
            yield from flatten_base(element)

    yield base
