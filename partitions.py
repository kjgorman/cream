import random
import numpy as np

def pairs(l):
    """
    Returns the input list split into pairs of sequential
    elements, along with a list of the remaining element if
    len(l) % 2 == 1.

    :example pairs([1,2,3])   -> ([(1,2)], [3])
             pairs([1,2,3,4]) -> ([(1,2),(3,4)], [])
    """
    resulting = []
    current = None

    for elem in l:
        if not (current is None):
            resulting.append((current, elem))
            current = None
        else:
            current = elem

    return (resulting, [] if current is None else [current])

def halves(l):
    """
    Returns the input list split into two halves, with the
    invariant that if f, l = halves(i) then len(f) <= len(l)
    """
    splitPoint = len(l) / 2
    return (l[:splitPoint], l[splitPoint:])

def choose(data, size):
    """
    Returns a random (with repetition) selection of elements
    of length min(size, len(data))
    """
    return [ data[np.random.randint(0, len(data))] for _ in xrange(0, size) ]
