
import heapq


def can_attend_all(events):
    """
    Return True if a person can attend all events
    without overlaps; otherwise, return False.
    """
    if not events:
        return True

    sorted_events = sorted(events, key=lambda event: event[0])

    for i in range(1, len(sorted_events)):
        previous_end = sorted_events[i - 1][1]
        current_start = sorted_events[i][0]

        if previous_end > current_start:
            return False

    return True


def min_rooms_required(events):
    """
    Return the minimum number of rooms required
    to schedule all events without overlapping.
    """
    if not events:
        return 0

    sorted_events = sorted(events, key=lambda event: event[0])

    # Min-heap storing end times of occupied rooms.
    end_times = []
    max_rooms = 0

    for start_time, end_time in sorted_events:

        # Free all rooms whose meetings have ended.
        while end_times and end_times[0] <= start_time:
            heapq.heappop(end_times)

        # Allocate a room to the current event.
        heapq.heappush(end_times, end_time)

        # Track the maximum number of rooms in use.
        max_rooms = max(max_rooms, len(end_times))

    return max_rooms


# Example usage
events = [(9, 11), (9, 10), (10, 12), (10, 11)]

print(can_attend_all(events))      # False
print(min_rooms_required(events))  # 3
