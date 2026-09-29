# GTK's native code resolves these bridge classes and members by name.
# Keep the JNI bridge, not every Java class in the application. Helpers such as
# SystemFilesystem and ImContext$ImeConnection remain eligible for optimization.
-keep,includedescriptorclasses class org.gtk.android.RuntimeApplication {
    native <methods>;
}
-keep,includedescriptorclasses class org.gtk.android.GlibContext {
    native <methods>;
}
-keep,includedescriptorclasses class org.gtk.android.ToplevelActivity { *; }
-keep,includedescriptorclasses class org.gtk.android.ToplevelActivity$* { *; }
-keep,includedescriptorclasses class org.gtk.android.ClipboardProvider$* { *; }
-keep,includedescriptorclasses class org.gtk.android.ImContext { *; }
-keep,includedescriptorclasses class org.gtk.android.ImContext$SurroundingRetVal { *; }

# Preserve any additional annotated entrypoints introduced by the GTK bridge.
-keep @androidx.annotation.Keep class * { *; }
-keepclasseswithmembers,includedescriptorclasses class * {
    @androidx.annotation.Keep <methods>;
}
-keepclasseswithmembers,includedescriptorclasses class * {
    @androidx.annotation.Keep <fields>;
}
-keepattributes RuntimeVisibleAnnotations,RuntimeInvisibleAnnotations,AnnotationDefault,InnerClasses,EnclosingMethod
