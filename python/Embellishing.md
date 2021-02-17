
# Embellishing

## Why

When you need to add functionality to different types of data that also need to be
perpetual, carrying beyond the original value. Then embellishing a type with
new functionality could be a good way to introduce new functionality and new
abstractions.

## How

### Functors as containers

We will use a simplified model of Functors where they act as a container, a
container with extra information.


Excusing the verbose type annotation in python you get this:

``` python
from __future__ import annotations
from typing import TypeVar, Generic

F = TypeVar('F')
T = TypeVar('T')
FunctorType = TypeVar('FunctorType', bound='Functor')

class Functor:
    """
    >>> functor.map(str)
    '42'
    """
    def map(self: FunctorType[F], f: Callable[[F], T]) -> FunctorType[T]:
        pass
```

A container that can take any Callable that takes one argument of the contained
type and then returns a new value. This lets the Functor preserve structure and
lets you reuse code that don't know about your Functor.
