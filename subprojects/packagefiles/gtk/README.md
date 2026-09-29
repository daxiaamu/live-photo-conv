# Android save dialog filename patch

`android-save-filename.patch` applies to the GTK revision in `subprojects/gtk.wrap`.
That revision launches `ACTION_CREATE_DOCUMENT` without `Intent.EXTRA_TITLE`,
so `Gtk.FileDialog.initial_name` never reaches Android's document picker.
Some providers then create a file named `invalid` with no extension.

The patch passes the chooser's current name as `EXTRA_TITLE` for save dialogs.
It uses GTK's UTF-8 to Java conversion helper so Unicode filenames are preserved.
Open-file and directory selection are unchanged. Meson applies the patch through
`diff_files`; keep it when refreshing the pinned GTK revision until upstream
provides equivalent handling.

## Device regression check

Build a fresh Android APK with the existing Android CI/Pixiewood workflow and
install it on the affected phone:

1. Select a video and choose Make Live Photo.
2. Confirm the system save dialog suggests `MVIMG_live_photo.jpg`.
3. Save inside the original folder at the root of shared storage (the reported
   folder is named `live图片`).
4. Confirm the saved file has the suggested name and `.jpg` extension, is not
   empty, and can be opened as a motion photo in a compatible gallery.
5. Repeat using a Chinese filename ending in `.jpg`.
6. Repeat saving the default name in the same folder; confirm the provider's
   duplicate-name handling preserves the extension and existing file contents.
7. Cancel the save dialog; confirm no conversion starts. Also verify video
   selection and extraction directory selection still work.

Patch application can be checked against the pinned GTK checkout with:

```sh
git apply --check --directory=subprojects/gtk subprojects/packagefiles/gtk/android-save-filename.patch
```

If Meson has already applied the patch, check with `--reverse` instead.

## Android localization

`android-locale.patch` initializes gettext's `LANGUAGE` preference from Android's
configuration before entering GTK. Simplified Chinese variants use `zh_CN`;
English stops fallback to a secondary language. Changes take effect on restart.
The application resolves catalogs relative to GTK's extracted asset data directory
and rebinds GTK/libadwaita domains after toolkit initialization.

Pixiewood must install both `runtime` and `i18n` Meson tags. After cloning the
`android36` builder, apply the repository's build patch before running it:

```sh
git -C pixiewood-tool apply ../build-aux/pixiewood-i18n.patch
```

The Android workflow applies this patch and runs
`python3 build-aux/check-apk-translations.py APK...` against the final APKs.
For device checks, restart on a Simplified Chinese system and check the launcher
name, window title, Make/Extract/Repair pages, error confirmation button and About
dialog. Restart on an English system with Chinese as a secondary language and
confirm English remains selected. Device validation is still required after a
fresh APK build; Java/catalog checks alone do not prove the rendered UI.
