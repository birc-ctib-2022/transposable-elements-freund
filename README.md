[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9491095&assignment_repo_type=AssignmentRepo)
# Project 5: Simulating transposable elements

In the last project, we imagine that someone has hired us to help out with simulating a genome containing [transposable elements]. (I know people who has such strange interests, so it is not beyond the realm of possibilities).

We won’t do anything complicated, this is just an exercise after all, but we will want to simulate TEs as stretches of DNA that can copy themselves elsewhere in the genome.

Our employer already has most of the simulator up and running. She has a program that randomly picks operations to do—insert a TE ab initio, copy a TE, or disable one with a mutation—but she needs us to program a representation of a genome to track where the TEs are.

There are multiple ways to do this, but you should implement at least two: one based Python lists, where each nucleotide is represented by one entry in a list, and one based on linked lists, where each nucleotide is represented by a link. If you feel ambitious, you can try others (for example keeping track of ranges of a genome with the same annotation so you don’t need to explicitly represent each nucleotide).

## Genome interface

A genome should be represented as a class that implements the following methods:

```python
class Genome(ABC):
    """Representation of a circular enome."""

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
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        ...  # not implemented yet

```

The `ABC` and `@abstractmethod` just means that this class is not something you can use by itself, but that another class must implement the details. In `src/genome.py` you will find templates for a Python list tand a linked list implementation (without the actual implementation, because you have to implement them).

You are free to implement the genome classes however you want, and using whateer auxilary data structures you desire, as long as one uses a Python list with an element for each nucleotide and the other a linked list with a link for each nucleotide. If you want to implement a third (or fourth or fifth...) version, you are very welcome to do so as well.

## Complexity

When you have implemented the two (or more) classes, describe the complexity of each operation as a function of the genome size (at the time of the operation), and the size of the TE involved (and when copying, the offset you are copying). Put the description here:

For notation on complexity, n will denote the size of the genome, m is the size of the TE

### Python list

```python
def __init__(self, n: int):
        """Create a new genome with length n."""
        self.genome = n * ["-"] # O(n)
        self.te_identities = {} # O(1)
        self.te_count = 0 # O(1)
```
**\_\_init\_\_ complexity:** $O(n)$
___

```python
def insert_te(self, pos: int, length: int) -> int:
        pos = pos % len(self.genome) # O(1)
        active_tes = list(self.te_identities.items()) # O(k)
        for id, te_range in active_tes: # O(k)
            start, end = te_range # O(1)
            if start <= pos < end: # O(1)
                self.genome[start:end] = (end - start) * ["x"] # O(n + m)
                self.te_identities.pop(id) # O(1)
                continue
            if start > pos: # O(1)
                self.te_identities[id] = (start + length, end + length) # O(1)
        self.te_count += 1 # O(1)
        self.te_identities[self.te_count] = (pos, pos + length) # O(1)
        self.genome = self.genome[:pos] + length * ["A"] + self.genome[pos:] # O(n + m)
        return self.te_count
```
**insert_te complexity:** $O(k(n+m))$
___
```python
  def copy_te(self, te: int, offset: int) -> int | None:
        if self.te_identities[te]: # O(1)
            te_range = self.te_identities[te] # O(1)
            start, end = te_range # O(1)
            copy_length = end - start # O(1)
            copy_pos = start + offset # O(1)
        return self.insert_te(copy_pos, copy_length)
```
**copy_te complexity:** $O(1)/O(k(n+m))$

While most of the copy-function can be completed in constant time, it also inherits the complexity of the insert function as a final step.
___
```python
def disable_te(self, te: int) -> None:
        if self.te_identities[te]: # O(1)
            te_range = self.te_identities.pop(te) # O(1)
            start, end = te_range # O(1)
            self.genome[start:end] = (end - start) * ['x'] # O(k + n)
```
**disable_te complexity:** $O(k+n)$
___
```python
    def active_tes(self) -> list[int]:
        return list(self.te_identities.keys())
```
**active_tes complexity:** $O(k)$
___
```python
def __len__(self) -> int:
        return len(self.genome)
```
**\_\_len\_\_ complexity:** $O(1)$
___
```python
def __str__(self) -> str:
        return "".join(self.genome)
```
**\_\_str\_\_ complexity:** $O(n)$
___

### Doubly-linked list

```python
def __init__(self, n: int):
        self.head = Link(None, None, None) # O(1)
        self.head.next = self.head # O(1)
        self.head.prev = self.head # O(1)
        self.length = n # O(1)
        self.te_identities = {} # O(1)
        self.te_count = 0 # O(1)
        for _ in range(n): # O(n)
            insert_after(self.head.prev, "-") # O(1)
```
**\_\_init\_\_ complexity:** $O(n)$
___
```python
def insert_te(self, pos: int, length: int) -> int:
        active_tes = list(self.te_identities.items()) # O(k)
        for id, te_range in active_tes: # O(k)
            start, end = te_range # O(1)
            if start <= pos < end: # O(1)
                self.disable_te(id)
                continue
            if start > pos: # O(1)
                self.te_identities[id] = (start + length, end + length) # O(1)
        self.te_count += 1 # O(1)
        self.te_identities[self.te_count] = (pos, pos + length) # O(1)
        current_link = self.head.next # O(1)
        for _ in range(pos - 1): # O(n)
            current_link = current_link.next # O(1)
        for _ in range(length): # O(m)
            insert_after(current_link, 'A') # O(1)
            current_link = current_link.next # O(1)
        self.length = self.length + length # O(1)
        return self.te_count
```
**insert_te complexity:** $O(k+n+m)$
___
```python
def copy_te(self, te: int, offset: int) -> int | None:
        if self.te_identities[te]: # O(1)
            te_range = self.te_identities[te] # O(1)
            start, end = te_range # O(1)
            copy_length = end - start # O(1)
            copy_pos = start + offset # O(1)
            if offset > 0: # O(1)
                return self.insert_te(copy_pos, copy_length)
            if (start + offset) < 0: # O(1)
                copy_pos = self.length + start + offset # O(1)
                return self.insert_te(copy_pos, copy_length)
            copy_pos = start + offset # O(1)
            return self.insert_te(copy_pos, copy_length)
```
**copy_te complexity:** $O(1)/O(k + n + m))$

While most of the copy-function can be completed in constant time, it also inherits the complexity of the insert function
___
```python
def disable_te(self, te: int) -> None:
        if self.te_identities[te]: # O(1)
            te_range = self.te_identities.pop(te) # O(1) average / O(n) amortized worst case
            start, end = te_range # O(1)
            current_link = self.head.next # O(1)
            for _ in range(start): # O(n)
                current_link = current_link.next # O(1)
            for _ in range(end - start): # O(m)
                current_link.val = 'x' # O(1)
                current_link = current_link.next # O(1)
```
**disable_te complexity:** $O(n + m)$
___
```python
def active_tes(self) -> list[int]:
        return list(self.te_identities.keys())
```
**active_tes complexity:** $O(k)$
___
```python
def __len__(self) -> int:
        return self.length
```
**\_\_len\_\_ complexity:** $O(1)$
___
```python
def __str__(self) -> str:
        links = []
        pos = self.head.next
        for _ in range(self.length):
            links.append(pos.val)
            pos = pos.next
        return "".join(links)
```
**\_\_str\_\_ complexity:** $O(n)$
___


In `src/simulate.py` you will find a program that can run simulations and tell you actual time it takes to simulate with different implementations. You can use it to test your analysis. You can modify the parameters to the simulator if you want to explore how they affect the running time.
