class _Node:
    """A node in the doubly linked list used by LRUCache."""

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """
    An LRU (Least Recently Used) cache.

    The cache stores at most `capacity` key-value pairs.
    The most recently used item is kept near the front of the list,
    and the least recently used item is kept near the back.
    """

    def __init__(self, capacity: int):
        # Treat negative capacity as zero.
        self.capacity = max(0, capacity)

        # Maps each key to its node in the doubly linked list.
        self.nodes = {}

        # Sentinel nodes: real nodes are stored between these two.
        self.head = _Node()
        self.tail = _Node()

        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: _Node) -> None:
        """Remove a node from its current position in the list."""
        previous_node = node.prev
        next_node = node.next

        previous_node.next = next_node
        next_node.prev = previous_node

    def _add_to_front(self, node: _Node) -> None:
        """Insert a node immediately after the head sentinel."""
        first_node = self.head.next

        node.prev = self.head
        node.next = first_node

        self.head.next = node
        first_node.prev = node

    def _mark_as_recently_used(self, node: _Node) -> None:
        """Move an existing node to the front of the list."""
        self._remove(node)
        self._add_to_front(node)

    def get(self, key: int) -> int:
        """
        Return the value for `key`, or -1 if the key is not in the cache.

        A successful get marks the item as recently used.
        """
        node = self.nodes.get(key)

        if node is None:
            return -1

        self._mark_as_recently_used(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        """
        Add or update a key-value pair.

        If the cache exceeds its capacity, evict the least recently used item.
        """
        if self.capacity == 0:
            return

        existing_node = self.nodes.get(key)

        if existing_node is not None:
            # Update the existing entry and mark it as recently used.
            existing_node.value = value
            self._mark_as_recently_used(existing_node)
            return

        # Add the new entry at the front, making it most recently used.
        new_node = _Node(key, value)
        self.nodes[key] = new_node
        self._add_to_front(new_node)

        # If over capacity, evict the least recently used entry.
        if len(self.nodes) > self.capacity:
            least_recently_used = self.tail.prev
            self._remove(least_recently_used)
            del self.nodes[least_recently_used.key]


# Example usage:
cache = LRUCache(2)

cache.put(1, 10)
cache.put(2, 20)

print(cache.get(1))  # 10; key 1 is now the most recently used

cache.put(3, 30)     # Evicts key 2, the least recently used key

print(cache.get(2))  # -1; key 2 was evicted
print(cache.get(3))  # 30