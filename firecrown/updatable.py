"""Parameters that can be updated, and collections of them.

Abstract class :class:`Updatable` is the base class from which any class in Firecrown
that supports updating from a :class:`ParamsMap` should inherit. Such classes are
expected to change state only in through their implementation of :python:`_update`
(including any other private methods used to implement :python:`_update`). Other
functions should not change the data of :class:`Updatable` objects.

:class:`UpdatableCollection` is a subclass of the built-in list. It implements the
:class:`Updatable` interface by calling :python:`update()` on each element it contains.
The :python:`append()` member is overridden to make sure that only objects which are of
a type that implements :class:`Updatable` can be appended to the list.

"""

from __future__ import annotations
from typing import final
from abc import ABC, abstractmethod
from collections import UserList
from .parameters import ParamsMap, RequiredParameters


class Updatable(ABC):
    """Abstract class Updatable is the base class for Updatable objects in Firecrown.

    Any class in Firecrown that supports updating from a ParamsMap should
    inherit. Such classes are expected to change state only in through their
    implementation of _update (including any other private methods used to
    implement _update). Other functions should not change the data of Updatable
    objects.

    """

    @final
    def update(self, params: ParamsMap):
        """Update self by calling the abstract _update() method.

        :param params: new parameter values
        """
        self._update(params)

    @abstractmethod
    def _update(self, params: ParamsMap) -> None:  # pragma: no cover
        """Abstract method to be implemented by all concrete classes to update
        self.

        Concrete classes must override this, updating themselves from the given
        ParamsMap. If the supplied ParamsMap is lacking a required parameter,
        an implementation should raise a TypeError.

        The base class implementation does nothing.

        :param params: a new set of parameter values
        """

    @abstractmethod
    def required_parameters(self) -> RequiredParameters:  # pragma: no cover
        """Return a RequiredParameters object containing the information for
        this Updatable. This method must be overridden by concrete classes.

        The base class implementation returns an empty RequiredParameters.
        """
        return RequiredParameters([])


class UpdatableCollection(UserList):

    """UpdatableCollection is a list of Updatable objects and is itself
    Updatable.

    Every item in an UpdatableCollection must itself be Updatable. Calling
    update on the collection results in every item in the collection being
    updated.
    """

    def __init__(self, iterable=None):
        """Initialize the UpdatableCollection from the supplied iterable.

        If the iterable contains any object that is not Updatable, a TypeError
        is raised.

        :param iterable: An iterable that yields Updateable objects
        """
        super().__init__(iterable)
        for item in self:
            if not isinstance(item, Updatable):
                raise TypeError(
                    "All the items in an UpdatableCollection must be updatable"
                )

    @final
    def update(self, params: ParamsMap):
        """Update self by calling update() on each contained item.

        :param params: new parameter values
        """
        for updatable in self:
            updatable.update(params)

    @final
    def required_parameters(self) -> RequiredParameters:
        """Return a RequiredParameters object formed by concatenating the
        RequiredParameters of each contained item.
        """
        result = RequiredParameters([])
        for updatable in self:
            result = result + updatable.required_parameters()

        return result

    def append(self, item: Updatable) -> None:
        """Append the given item to self.

        If the item is not Updatable a TypeError is raised.

        :param item: new item to be appended to the list
        """
        if not isinstance(item, Updatable):
            raise TypeError(
                "Only updatable items can be appended to an UpdatableCollection"
            )
        super().append(item)

    def __setitem__(self, key, value):
        """Set self[key] to value; raise TypeError if Value is not Updatable."""
        if not isinstance(value, Updatable):
            raise TypeError(
                "Values inserted into an UpdatableCollection must be Updatable"
            )
        super().__setitem__(key, value)
