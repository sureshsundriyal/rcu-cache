rcu-python
==========

The **rcu-python** module implements a multi-producer, multi-consumer
thread-safe FIFO cache modeled after an OrderedDict. The object features
lock-less reads and the writes are guarded by a lock leading to fast reads and
thread-safe writes.

Example:
--------
```py
   >>> from rcu import RCUCache

# Setting the maxsize to 0 results in an unlimited sized cache. The constructor
# also accepts 
   >>> cache = RCUCache(maxsize=2, items=None)
   >>> print(cache)
   RCUCache(maxsize=2, items=OrderedDict())

   >>> cache[2] = 10
   >>> cache[10] = 200
   >>> print(cache)
   RCUCache(maxsize=2, items=OrderedDict([(2, 10), (10, 200)]))

# Adding another element will get rid of the first element that was added.
   >>> cache[50] = 1000
   >>> print(cache)
   RCUCache(maxsize=2, items=OrderedDict([(10, 200), (50, 1000)]))
   >>> len(cache)
   2

# The object deliberately does not feature a getter method, since checking for
# the existence of an element and then accessing that element is inherently a
# race condition. Simply access the element and catch the `KeyError` if you need
# to test for membership.
   >>> try:
   ...     cache[20]
   ... except KeyError as e:
   ...     print("Key %s not found in the cache" % e)
   Key 20 not found in the cache

```

In addition to the above methods, the **RCUCache** object also features the
following methods:

* ```clear()```
  Remove all items from the cache.

* ```copy()```
  Returns a shallow copy of the cache.

* ```popitem(last=True)```
  The `popitem()` method for ordered dictionaries returns and removes a (key,
  value) pair. The pairs are returned in LIFO order if last is true or FIFO
  order if false.

* ```pop(key[, default])```
  If key is in the dictionary, remove it and return its value, else return
  default. If default is not given and key is not in the dictionary, a KeyError
  is raised.

* ```update([other])```
  Update the dictionary with the key/value pairs from other, overwriting
  existing keys. The `maxsize` is honored during an update.
