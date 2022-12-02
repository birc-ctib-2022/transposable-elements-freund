"""A circular genome for simulating transposable elements."""
from __future__ import annotations
from abc import (
    # A tag that says that we can't use this class except by specializing it
    ABC,
    # A tag that says that this method must be implemented by a child class
    abstractmethod
)

from typing import(
    Generic, TypeVar
)


class Genome(ABC):
    """Representation of a circular genome."""

    def __init__(self, n: int):
        """Create a genome of size n."""
        ...  # not implemented yet

    @abstractmethod
    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        ...  # not implemented yet

    @abstractmethod
    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        ...  # not implemented yet

    @abstractmethod
    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # not implemented yet

    @abstractmethod
    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        ...  # not implemented yet

    @abstractmethod
    def __len__(self) -> int:
        """Get the current length of the genome."""
        ...  # not implemented yet

    @abstractmethod
    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immediately followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        ...  # not implemented yet


class ListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using Python's built-in lists
    """

    def __init__(self, n: int):
        """Create a new genome with length n."""
        self.genome = n * ["-"]
        self.te_identities = {}
        self.te_count = 0


    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """

        if pos > len(self.genome):
            raise ValueError("Position is out of range of genome.")

        pos = pos % len(self.genome) # Circularize genome for copy function

        active_tes = list(self.te_identities.items())
        for id, te_range in active_tes:
            start, end = te_range

            if start <= pos < end:
                self.genome[start:end] = (end - start) * ["x"]
                self.te_identities.pop(id)
                continue

            if start > pos:
                # Define new range for TEs that are positioned later
                # in the genome than the newly inserted one
                self.te_identities[id] = (start + length, end + length)

        self.te_count += 1
        self.te_identities[self.te_count] = (pos, pos + length)
        self.genome = self.genome[:pos] + length * ["A"] + self.genome[pos:]

        return self.te_count


    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        if te not in self.te_identities:
            return None

        te_range = self.te_identities[te] # Get positions for TE
        start, end = te_range

        copy_length = end - start # Length of copy
        copy_pos = start + offset # Position of copy

        return self.insert_te(copy_pos, copy_length)



    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        if self.te_identities[te]:

            te_range = self.te_identities.pop(te)
            start, end = te_range

            self.genome[start:end] = (end - start) * ['x']


    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        return list(self.te_identities.keys())

    def __len__(self) -> int:
        """Current length of the genome."""
        return len(self.genome)

    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immediately followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        return "".join(self.genome)



T = TypeVar('T')

class Link(Generic[T]):
    """Doubly linked link."""
    val: T
    prev: Link[T]
    next: Link[T]

    def __init__(self, val: T, p: Link[T], n: Link[T]):
        """Create new link and link up previous and next."""
        self.val = val
        self.prev = p
        self.next = n


def insert_after(link: Link[T], val: T) -> None:
    """Add new link containing val after link."""
    new_link = Link(val, link, link.next)
    new_link.prev.next = new_link
    new_link.next.prev = new_link


def remove_link(link: Link[T]) -> None:
    """Remove link from list."""
    link.prev.next = link.next
    link.next.prev = link.prev

class LinkedListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using linked lists.
    """

    head = Link[T]


    def __init__(self, n: int):
        """Create a new genome with length n."""
        self.head = Link(None, None, None)
        self.head.next = self.head
        self.head.prev = self.head

        self.length = n

        self.te_identities = {}
        self.te_count = 0

        for _ in range(n):
            insert_after(self.head.prev, "-")


    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """

        if pos > self.length:
            raise ValueError("Position is out of range of genome.")

        active_tes = list(self.te_identities.items())
        for id, te_range in active_tes:
            start, end = te_range

            if start <= pos < end:
                self.disable_te(id)
                continue

            if start > pos:
                # Define new range for TEs that are positioned later
                # in the genome than the newly inserted one
                self.te_identities[id] = (start + length, end + length)

        self.te_count += 1
        self.te_identities[self.te_count] = (pos, pos + length)

        # Insert new TE
        current_link = self.head.next
        for _ in range(pos - 1): # Go to pos
            current_link = current_link.next
        for _ in range(length):
            insert_after(current_link, 'A')
            current_link = current_link.next

        self.length = self.length + length # New genome length

        return self.te_count


    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        if te not in self.te_identities:
            return None

        te_range = self.te_identities[te]
        start, end = te_range

        copy_length = end - start
        copy_pos = start + offset

        if offset > 0:
            return self.insert_te(copy_pos, copy_length)

        if (start + offset) < 0:
            copy_pos = self.length + start + offset
            return self.insert_te(copy_pos, copy_length)

        copy_pos = start + offset
        return self.insert_te(copy_pos, copy_length)



    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        if self.te_identities[te]:

            te_range = self.te_identities.pop(te)
            start, end = te_range

            current_link = self.head.next
            for _ in range(start):
                current_link = current_link.next

            for _ in range(end - start):
                current_link.val = 'x'
                current_link = current_link.next


    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        return list(self.te_identities.keys())

    def __len__(self) -> int:
        """Current length of the genome."""
        return self.length

    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immediately followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """

        links = []
        pos = self.head.next
        for _ in range(self.length):
            links.append(pos.val)
            pos = pos.next
        return "".join(links)

