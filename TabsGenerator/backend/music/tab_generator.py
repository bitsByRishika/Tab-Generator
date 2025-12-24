def generate_tab_events(events, step=0.1):
    """
    Convert note events into tab column events.

    Input events:
    {
        "note": "G4",
        "start": 6.6,
        "end": 8.6,
        "string": 1,
        "fret": 3
    }

    Output tab events:
    {
        "string": 1,
        "fret": 3,
        "start_col": 66,
        "end_col": 86
    }
    """

    tab_events = []

    for e in events:
        if "string" not in e or "fret" not in e:
            continue

        start_col = int(e["start"] / step)
        end_col = int(e["end"] / step)

        tab_events.append({
            "string": e["string"],
            "fret": e["fret"],
            "start_col": start_col,
            "end_col": end_col
        })

    return tab_events


def build_ascii_tab(tab_events, total_cols):
    """
    Build ASCII guitar tabs from tab events.
    """

    # Initialize empty tab grid
    grid = {
        1: ["-"] * total_cols,  # high E
        2: ["-"] * total_cols,  # B
        3: ["-"] * total_cols,  # G
        4: ["-"] * total_cols,  # D
        5: ["-"] * total_cols,  # A
        6: ["-"] * total_cols,  # low E
    }

    for e in tab_events:
        s = e["string"]
        f = str(e["fret"])

        col = e["start_col"]

        # Handle multi-digit frets (10, 11, 12)
        if len(f) == 1:
            grid[s][col] = f
        else:
            grid[s][col] = f[0]
            if col + 1 < total_cols:
                grid[s][col + 1] = f[1]

    # Convert grid to printable lines
    ascii_tab = {
        1: "e|" + "".join(grid[1]),
        2: "B|" + "".join(grid[2]),
        3: "G|" + "".join(grid[3]),
        4: "D|" + "".join(grid[4]),
        5: "A|" + "".join(grid[5]),
        6: "E|" + "".join(grid[6]),
    }

    return ascii_tab
