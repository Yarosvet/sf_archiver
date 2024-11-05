"""Algorithms of assigning codes"""
import heapq
from typing import BinaryIO


# TODO: Do some make-up here


def assign_shannon_fano(
        dist_group: list[tuple[bytes, float]],
        prefix: str = ""
) -> dict[bytes, str]:
    """
    Assign syms to their binary codes using Shannon-Fano algorithm
    :param dist_group: Tuples (letter, distribution)
    :param prefix: Current prefix
    :return: Dictionary (sym:code)
    """
    _dist = list(sorted(dist_group, key=lambda x: x[1]))

    if len(_dist) == 0:
        return {}
    elif len(_dist) == 1:
        return {_dist[0][0]: prefix}
    elif len(_dist) == 2:
        return {_dist[0][0]: prefix + "0", _dist[1][0]: prefix + "1"}

    line = len(_dist) - 1
    for i in range(1, len(_dist) - 1):
        # Calculate the difference between the sum of the left and right parts divided by i
        delta_i = abs(sum(x[1] for x in _dist[:i]) - sum(x[1] for x in _dist[i:]))
        # Divided by i+1
        delta_i1 = abs(sum(x[1] for x in _dist[:i + 1]) - sum(x[1] for x in _dist[i + 1:]))

        if delta_i <= delta_i1:
            line = i
            break

    return assign_shannon_fano(_dist[:line], prefix=prefix + "0") | assign_shannon_fano(_dist[line:],
                                                                                        prefix=prefix + "1")


class HuffmanNode:
    def __init__(self, symbol=None, frequency=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency


def build_huffman_tree(dist_group: list[tuple[bytes, float]]) -> HuffmanNode:
    # Create a priority queue of nodes
    priority_queue = [HuffmanNode(char, f) for char, f in dist_group]
    heapq.heapify(priority_queue)

    # Build the Huffman tree
    while len(priority_queue) > 1:
        left_child = heapq.heappop(priority_queue)
        right_child = heapq.heappop(priority_queue)
        merged_node = HuffmanNode(frequency=left_child.frequency + right_child.frequency)
        merged_node.left = left_child
        merged_node.right = right_child
        heapq.heappush(priority_queue, merged_node)

    return priority_queue[0]


def generate_huffman_codes(node, code="", huffman_codes=None):
    if huffman_codes is None:
        huffman_codes = {}
    if node is not None:
        if node.symbol is not None:
            huffman_codes[node.symbol] = code
        generate_huffman_codes(node.left, code + "0", huffman_codes)
        generate_huffman_codes(node.right, code + "1", huffman_codes)

    return huffman_codes


def assign_huffman(
        dist_group: list[tuple[bytes, float]],
        prefix: str = ""
) -> dict[bytes, str]:
    """
    Assign syms to their binary codes using Huffman algorithm
    :param dist_group: Tuples (letter, distribution)
    :param prefix: Current prefix
    :return: Dictionary (sym:code)
    """
    root = build_huffman_tree(dist_group)
    return generate_huffman_codes(root)


def count_distribution(if_stream: BinaryIO) -> list[tuple[bytes, float]]:
    # Count statistics
    stats: dict[bytes, int] = {}
    while sym := if_stream.read(1):
        stats[sym] = stats.get(sym, 0) + 1
    if_stream.seek(0)  # Reset to start
    # Count distribution
    total = sum(stats.values())
    dist = {k: v / total for k, v in stats.items()}
    if len(dist) == 1:
        raise ValueError("Single symbol content")
    return [(k, v) for k, v in dist.items()]
