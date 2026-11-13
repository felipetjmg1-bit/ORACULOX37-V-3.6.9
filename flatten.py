"""Helpers for traversing Speckle object trees."""

from collections.abc import Iterable, Iterator, Mapping
from typing import Any


def _children(node: Any) -> list[Any]:
    """Return children from the supported Speckle elements properties."""
    value = None
    for attribute in ("elements", "@elements"):
        try:
            value = getattr(node, attribute)
        except (AttributeError, TypeError):
            continue
        if value is not None:
            break

    if value is None:
        return []
    if isinstance(value, Mapping):
        return list(value.values())
    if isinstance(value, (str, bytes, bytearray)):
        return []
    if isinstance(value, Iterable):
        return list(value)
    return [value]


def flatten_base(base: Any) -> Iterator[Any]:
    """Yield each object in a Speckle ``elements`` tree once.

    Traversal is iterative to avoid recursion-depth failures and tracks object
    identity to prevent cycles from causing an infinite loop. The root object is
    included in the result. Mappings and ordinary collections are traversed but
    are not themselves yielded as model objects.
    """
    if base is None:
        return

    stack = [base]
    visited: set[int] = set()

    while stack:
        node = stack.pop()
        if node is None:
            continue
        if isinstance(node, (str, bytes, bytearray)):
            continue

        identity = id(node)
        if identity in visited:
            continue
        visited.add(identity)

        if isinstance(node, Mapping):
            stack.extend(reversed(list(node.values())))
            continue
        if isinstance(node, (list, tuple, set, frozenset)):
            stack.extend(reversed(list(node)))
            continue

        yield node

        children = _children(node)
        stack.extend(reversed(children))
