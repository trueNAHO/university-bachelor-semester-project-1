#!/usr/bin/env python

# The `BoxMultiLineEdit` class is a wrapper to draw a box around npyscreen's
# `MultiLineEdit` widget.

import npyscreen

class BoxMultiLineEdit(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLineEdit
