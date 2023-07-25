#!/usr/bin/env python

# Helper functions wrapped inside the `Lib` class.

class Lib:
    # Write `data` to the `filepath`.
    @staticmethod
    def string_to_file(data: str | None, filepath: str) -> str:
        with open(filepath, "w") as file:
            file.write(str(data) if data else "")
        return filepath
