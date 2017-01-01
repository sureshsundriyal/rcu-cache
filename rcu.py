#! /usr/bin/env python

__author__ = 'Suresh Sundriyal'
__license__ = 'CC0 - No rights reserved.'
__version__ = '0.0.1'

from threading import Lock
from collections import OrderedDict
from itertools import repeat

__all__ = ['RCUCache']

class RCUCache(object): # pylint: disable=too-few-public-methods
    '''
    TODO: Put in the class documentation.
    '''

    # The following makes the object unextendable.
    __slots__ = ('maxsize', 'odict', 'modification_guard', '_setattr')

    # The following values cannot be pickled.
    _unpicklable = set(['modification_guard', '_setattr'])

    def __setattr__(self, *args, **kwargs):
        # Override __setattr__ to make the object itself immutable.
        raise TypeError('%s is immutable' % self.__class__.__name__)

    __delattr__ = __setattr__

    def __init__(self, maxsize=None, items=None):
        if items is None:
            items = []
        super(self.__class__,
              self).__setattr__('_setattr',
                                super(self.__class__, self).__setattr__)
        # pylint: disable=no-member
        self._setattr('maxsize', maxsize)
        self._setattr('odict', OrderedDict(items))
        self._setattr('modification_guard', Lock())
        # pylint: enable=no-member

    def __getstate__(self):
        state = {}
        for var in set(self.__slots__) - self._unpicklable:
            state[var] = getattr(self, var)
        return state

    def __setstate__(self, state):
        super(self.__class__,
              self).__setattr__('_setattr',
                                super(self.__class__, self).__setattr__)
        # pylint: disable=no-member
        self._setattr('modification_guard', Lock())
        for var in state:
            self._setattr(var, state[var])
        # pylint: enable=no-member

    def __contains__(self, *args, **kwargs):
        '''
        Lookup is disabled since looking up an object and then accessing it is
        inherently a race condition.
        '''
        raise TypeError("Directly access the %s members to test for membership"
                        % self.__class__.__name__)

    def __getitem__(self, key):
        return self.odict[key] # pylint: disable=no-member

    def __setitem__(self, key, value):
        # pylint: disable=no-member
        with self.modification_guard:
            temp_odict = OrderedDict(self.odict)
            if self.maxsize and len(self.odict) == self.maxsize:
                temp_odict.popitem(last=False)
            temp_odict[key] = value
            self._setattr('odict', temp_odict)
        # pylint: enable=no-member

    def __delitem__(self, key):
        # pylint: disable=no-member
        with self.modification_guard:
            temp_odict = OrderedDict(self.odict)
            del temp_odict[key]
            self._setattr('odict', temp_odict)
        # pylint: enable=no-member

    def __repr__(self):
        # pylint: disable=no-member
        return '%s(maxsize=%s, items=%r)' % (self.__class__.__name__,
                                          self.maxsize, self.odict)
        # pylint: enable=no-member

    def __len__(self):
        return len(self.odict) # pylint: disable=no-member

    def clear(self):
        '''
        Clear out all the elements in the container.
        '''
        # pylint: disable=no-member
        with self.modification_guard:
            self._setattr('odict', OrderedDict())
        # pylint: enable=no-member

    def copy(self):
        '''
        Create a copy of the object
        '''
        return self.__class__(self.maxsize, self.odict) # pylint: disable=no-member

    def update(self, *args, **kwargs):
        # pylint: disable=no-member
        with self.modification_guard:
            temp_odict = OrderedDict(self.odict)
            temp_odict.update(*args, **kwargs)
            if self.maxsize and len(temp_odict) > self.maxsize:
                for _ in repeat(None, (len(temp_odict) - self.maxsize)):
                    temp_odict.popitem(last=False)
            self._setattr('odict', temp_odict)
        # pylint: enable=no-member

    def popitem(self, last=True):
        # pylint: disable=no-member
        with self.modification_guard:
            temp_odict = OrderedDict(self.odict)
            retval = temp_odict.popitem(last=last)
            self._setattr('odict', temp_odict)
            return retval
        # pylint: enable=no-member

    def pop(self, *args, **kwargs):
        # pylint: disable=no-member
        with self.modification_guard:
            temp_odict = OrderedDict(self.odict)
            retval = temp_odict.pop(*args, **kwargs)
            self._setattr('odict', temp_odict)
            return retval
        # pylint: enable=no-member

    def items(self, *args, **kwargs):
        tempRef = self.odict
        return tempRef.items()

    def __iter__(self, *args, **kwargs):
        tempRef = self.odict
        return iter(tempRef)
