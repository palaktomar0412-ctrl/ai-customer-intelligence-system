# How to Convert to a Mobile/Desktop App

## Complete Guide — All Conversion Options

---

## Option 1: PWA (Already Configured) ✅

The fastest path — no code changes needed, just build and deploy.

### Steps:
```bash
cd frontend
npm run build
npx serve dist
```

### To install on devices:
- **Android:** Open in Chrome → tap "Add to Home Screen"
- **iOS:** Open in Safari → tap Share → "Add to Home Screen"
- **Desktop:** Chrome → address bar shows "Install" icon

### Pros: No app store, instant updates, works on all platforms
### Cons: Limited hardware access (camera, GPS), no push notifications on iOS

---

## Option 2: Electron Desktop App (Windows/Mac/Linux)

Wraps the React app in a native desktop window.

### Steps:
```bash
cd frontend

# Install Electron
npm install electron --save-dev
npm install electron-builder --save-dev

# Update package.json scripts (see below)
# Run in development
npx electron .

# Build distributable
npx electron-builder --win     # Windows .exe installer
npx electron-builder --mac     # Mac .dmg
npx electron-builder --linux   # Linux .AppImage
```

### package.json additions:
```json
{
  "main": "electron.js",
  "scripts": {
    "electron": "electron .",
    "build:win": "electron-builder --win",
    "build:mac": "electron-builder --mac",
    "build:linux": "electron-builder --linux"
  },
  "build": {
    "appId": "com.customerintelligence.app",
    "productName": "Customer Intelligence",
    "directories": { "output": "release" },
    "files": ["dist/**/*", "electron.js"],
    "win": { "target": "nsis", "icon": "public/icon-512.png" },
    "mac": { "target": "dmg", "icon": "public/icon-512.png" },
    "linux": { "target": "AppImage", "icon": "public/icon-512.png" }
  }
}
```

### Pros: Full native access, distributable as .exe/.dmg/.AppImage
### Cons: Large bundle size (~150MB), separate builds per OS

---

## Option 3: Capacitor Mobile App (Android/iOS)

Uses the existing React build wrapped in a native shell.

### Steps:
```bash
cd frontend

# Install Capacitor
npm install @capacitor/core @capacitor/cli
npx cap init "CustomerIntel" "com.customerintelligence.app" --web-dir dist

# Build the React app first
npm run build

# Add platforms
npx cap add android
npx cap add ios

# Sync web assets to native projects
npx cap sync

# Open in IDE
npx cap open android    # Opens Android Studio
npx cap open ios        # Opens Xcode (Mac only)
```

### Build for release:
```bash
# Android
cd android && ./gradlew assembleRelease
# APK: android/app/build/outputs/apk/release/

# iOS (Mac only with Xcode)
npx cap open ios → Product → Archive
```

### Pros: Native shell, access to device APIs, Play Store/App Store ready
### Cons: Android Studio / Xcode required, iOS needs Mac

---

## Option 4: Tauri (Lightweight Desktop — Rust-based)

Modern alternative to Electron, much smaller binary.

### Steps:
```bash
cd frontend
npm install -D @tauri-apps/cli

# Requires Rust installed (https://rustup.rs)
npx tauri init
npx tauri build

# Produces .msi (Windows), .dmg (Mac), .deb (Linux)
# Binary size: ~5-10MB vs Electron's ~150MB
```

### Pros: Tiny binary, fast, memory efficient, Rust security
### Cons: Requires Rust toolchain, newer ecosystem

---

## Quick Comparison Table

| Approach | Platform | Size | Ease | Hardware Access |
|----------|----------|------|------|-----------------|
| **PWA** | All | ~1MB | ⭐⭐⭐⭐⭐ | Limited |
| **Electron** | Desktop | ~150MB | ⭐⭐⭐⭐ | Full |
| **Capacitor** | Mobile | ~10MB | ⭐⭐⭐ | Good |
| **Tauri** | Desktop | ~5MB | ⭐⭐⭐ | Full |

---

## Recommendation

| If you want... | Use this |
|----------------|----------|
| Quickest install on any device | **PWA** ✅ (already done) |
| Desktop app for demo/portfolio | **Electron** |
| Mobile app for Play Store | **Capacitor** |
| Lightweight desktop app | **Tauri** |
