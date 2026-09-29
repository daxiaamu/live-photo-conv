#!/usr/bin/env python3
"""Verify R8 ran and did not rename GTK classes looked up through JNI."""
from pathlib import Path
import re
import sys

BRIDGES = (
    'RuntimeApplication', 'GlibContext', 'ToplevelActivity',
    'ToplevelActivity$GdkContext', 'ToplevelActivity$ToplevelView',
    'ToplevelActivity$ToplevelView$Surface',
    'ToplevelActivity$UnregisteredSurfaceException',
    'ClipboardProvider$ClipboardChangeListener',
    'ClipboardProvider$ClipboardBitmapDragShadow',
    'ClipboardProvider$ClipboardEmptyDragShadow',
    'ClipboardProvider$InternalClipdata',
    'ClipboardProvider$NativeDragIdentifier',
    'ImContext', 'ImContext$SurroundingRetVal',
)


def check(path):
    text = Path(path).read_text(encoding='utf-8')
    if '# compiler: R8' not in text:
        raise ValueError('Missing R8 compiler marker in mapping')
    classes = dict(re.findall(r'^([^\s#].*?) -> (.*?):$', text, re.MULTILINE))
    for name in BRIDGES:
        name = 'org.gtk.android.' + name
        if classes.get(name) != name:
            raise ValueError(f'JNI bridge missing or renamed: {name}')
    renamed = sum(before != after for before, after in classes.items())
    print(f'R8 mapping verified: {len(BRIDGES)} JNI class names preserved, {renamed} classes renamed.')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: check-r8-mapping.py MAPPING_FILE')
    check(sys.argv[1])
