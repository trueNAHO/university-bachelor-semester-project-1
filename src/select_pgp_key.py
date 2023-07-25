#!/usr/bin/env python

# The `SelectPgpKey` class is a wrapper for npyscreen's `SelectOne` widget that
# customises how it disaplys its values.

import npyscreen

class SelectPgpKey(npyscreen.SelectOne):
    # Display the key's type, ID, and UIDS.
    def display_value(self, value) -> str:
        return "{}\t{}\t{}".format(value.get("type"), value.get("keyid"),
                                   value.get("uids"))
