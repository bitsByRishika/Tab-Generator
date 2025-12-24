def wrap_ascii_tabs(ascii_tabs, width=70):
    """
    Break long ASCII tabs into multiple readable rows.

    ascii_tabs: dict {1:'e|...', 2:'B|...', ...}
    width: number of characters per row (excluding string label)
    """

    string_order = [1, 2, 3, 4, 5, 6]
    labels = {
        1: "e|",
        2: "B|",
        3: "G|",
        4: "D|",
        5: "A|",
        6: "E|",
    }

    # Strip labels
    raw = {s: ascii_tabs[s][2:] for s in string_order}
    total_len = len(raw[1])

    blocks = []

    for start in range(0, total_len, width):
        block = []
        for s in string_order:
            segment = raw[s][start:start + width]
            block.append(labels[s] + segment)
        blocks.append(block)

    return blocks
