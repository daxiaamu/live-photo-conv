#!/usr/bin/env python3
"""Enable R8 on the generated Pixiewood release project before Gradle runs."""
from pathlib import Path
import shutil
import sys


def configure(app):
    root = Path(__file__).resolve().parent.parent
    gradle = app / 'build.gradle'
    text = gradle.read_text(encoding='utf-8')
    original = 'release {\n            minifyEnabled false\n        }'
    optimized = '''release {
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }'''
    if text.count(original) != 1:
        raise ValueError('Unexpected Pixiewood release configuration; review before enabling R8')
    gradle.write_text(text.replace(original, optimized), encoding='utf-8')
    shutil.copyfile(root / 'android/proguard-rules.pro', app / 'proguard-rules.pro')
    # GTK may resolve theme resources from native code. Keep the small theme
    # surface while shrinking other Android resources; gettext assets are kept.
    raw = app / 'src/main/res/raw'
    raw.mkdir(parents=True, exist_ok=True)
    (raw / 'live_photo_conv_keep.xml').write_text(
        '<resources xmlns:tools="http://schemas.android.com/tools" '
        'tools:keep="@color/*,@style/*,@attr/*" />\n', encoding='utf-8')
    print('Enabled release R8 optimization and resource shrinking with GTK JNI keep rules.')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: configure-android-r8.py GENERATED_ANDROID_APP_DIR')
    configure(Path(sys.argv[1]))
