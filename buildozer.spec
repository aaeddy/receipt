[app]
title = 收据生成器
package.name = receiptgenerator
package.domain = org.receipt
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf,svg
version = 1.0.0
orientation = portrait
fullscreen = 0
presplash.filename = %(source.dir)s/data/presplash.png
icon.filename = %(source.dir)s/data/icon.png

[buildozer]
log_level = 2

[android]
permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.accepts_sdk_licenses = True

[android.meta]
android.manifest_placeholders = [:]

[android.gradle_dependencies]

[android.permissions]

[android.uses_sdk]
min_sdk_version = 21
target_sdk_version = 33

[ios]

[macos]

[windows]
