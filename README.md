# Mohammed_Sameer_Wahab_Avaloka_Assignment

## Final Discussion & Analysis

### 1. Time & Space Complexity

Let \\(n\\) represent the number of events in the scheduler and \\(C\\) represent the LRU cache's capacity.

| Function                     | Time Complexity    | Space Complexity     |
| ---------------------------- | ------------------ | -------------------- |
| `LRUCache.get(key)`          | \(O(1)\) average | \(O(1)\) auxiliary |
| `LRUCache.put(key, value)`   | \(O(1)\) average | \(O(1)\) auxiliary |
| `can_attend_all(events)`     | \(O(nlog n)\)   | \(O(n)\)           |
| `min_rooms_required(events)` | \(O(nlog n)\)   | \(O(n)\)           |

LRU Cache: Both `get()` and `put()` operate in \\(O(1)\\) average time because the hash map provides constant-time average lookups, while the doubly linked list supports constant-time insertion, removal, and repositioning of nodes. Evicting the least recently used item also takes \\(O(1)\\) time because it is located at the end of the list. The cache requires \\(O(C)\\) total space to store at most \\(C\\) entries, although each individual operation uses \\(O(1)\\) auxiliary space.

Event Scheduler: Both functions require \\(O(n\log n)\\) time because sorting dominates their execution time. In `can_attend_all()`, checking consecutive events takes an additional \\(O(n)\\) time. In `min_rooms_required()`, each event is inserted into the min-heap once and removed at most once, with each heap operation taking \\(O(\log n)\\) time. Both implementations use \\(O(n)\\) additional space for the sorted event list and, in the room calculation, the heap. The heap can contain up to \\(n\\) end times in the worst case.

The LRU complexities assume average-case hash map performance. Hash map operations can take longer in pathological collision scenarios.

### 2. Trade-offs: Why Combine a Hash Map and a Doubly Linked List for an LRU Cache?

A hash map and a doubly linked list complement each other by solving two different requirements of an LRU cache.

A hash map provides fast access to an entry using its key, with \\(O(1)\\) average lookup time. However, it does not inherently maintain the order in which entries were recently accessed.

A doubly linked list maintains the entries in usage order, with the most recently used item at the front and the least recently used item at the back. It allows nodes to be removed and repositioned in \\(O(1)\\) time when their references are already available. However, finding an arbitrary entry by its key would require an \\(O(n)\\) traversal if the list were used alone.

Combining the two solves both problems: the hash map points directly to each entry's linked-list node, while the list maintains the usage order and identifies the item to evict.

The main trade-off is additional memory and implementation complexity. Each entry requires both a hash map entry and a linked-list node, including its previous and next pointers. The implementation must also keep both structures synchronized during insertions, updates, and evictions. Despite this overhead, the combination is effective when fast lookups and predictable constant-time recency updates are important.

### 3. Future Proofing: Assigning Specific Room Numbers to Events

To assign room names such as "Room A" and "Room B", I would extend the existing scheduler to track room identities in addition to their availability times.

I would maintain two data structures:

- A min-heap of occupied rooms: Each entry would contain the meeting's end time and its assigned room identifier, such as `(end_time, room_name)`. This allows the scheduler to identify the room that becomes available first.
- A collection of available rooms: This would hold the identifiers of rooms whose meetings have finished and that can be reused.

The scheduler would process events in ascending order of start time. Before assigning a room to an event, it would release every room whose meeting ends at or before the event's start time, returning those room identifiers to the available-room collection.

If an available room exists, the scheduler would reuse it. Otherwise, it would allocate a new room and assign it a unique identifier. It would then add the room's new availability time to the min-heap and record the event-to-room assignment in a mapping or result list.

This approach preserves the \\(O(n\log n)\\) time complexity while providing explicit room assignments. The additional storage required for room identifiers and event assignments remains \\(O(n)\\) in the worst case. In a production system, I would also consider room capacities, equipment requirements, unavailable rooms, and reservation conflicts when selecting an available room.

### 4. Concurrency: Making the LRU Cache Thread-Safe

The current LRU cache implementation is designed for sequential operations. If multiple threads access or modify it simultaneously, they could interfere with one another while updating the hash map and doubly linked list.

For example, one thread might be moving a node to the front while another thread evicts that same node. This could leave the two data structures inconsistent or corrupt the linked-list pointers.

The simplest solution is to introduce a mutex or lock that protects the cache's shared state. Both `get()` and `put()` would acquire the lock before accessing or modifying the cache and release it after the entire operation is complete.

The lock must cover the complete operation, including all related hash map and linked-list changes. A successful `get()` also modifies the recency order, so it cannot be treated as a read-only operation. Similarly, `put()` must update the value, reposition nodes, and perform any necessary eviction while holding the lock.

This approach ensures that each operation behaves atomically from the perspective of other threads, preventing simultaneous modifications from leaving the cache in an inconsistent state. Its main trade-off is contention: threads may have to wait for the lock, reducing throughput when many threads access the cache concurrently.

For higher-concurrency workloads, more advanced techniques, such as finer-grained locking or sharded caches, could improve throughput. However, these approaches increase implementation complexity and require careful synchronization. A single lock around each complete cache operation is a suitable starting point because it prioritizes correctness and simplicity.
