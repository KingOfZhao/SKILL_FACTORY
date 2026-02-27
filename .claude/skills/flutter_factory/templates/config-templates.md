# Config 模板

## pubspec.yaml 模板（Riverpod 版本）

```yaml
name: project_name
description: A Flutter application.
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter

  # State Management
  flutter_riverpod: ^2.4.0

  # Bluetooth
  flutter_blue_plus: ^1.31.0
  permission_handler: ^11.0.0

  # UI Components
  fl_chart: ^0.66.0
  cupertino_icons: ^1.0.6

  # Utilities
  shared_preferences: ^2.2.0
  intl: ^0.18.0

  # Architecture
  freezed_annotation: ^2.4.0
  json_annotation: ^4.8.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

  # Code Generation
  build_runner: ^2.4.0
  freezed: ^2.4.0
  json_serializable: ^6.7.0

flutter:
  uses-material-design: true

  assets:
    - assets/images/
    - assets/icons/
```

## pubspec.yaml 模板（BLoC 版本）

```yaml
name: project_name
description: A Flutter application.
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter

  # State Management
  flutter_bloc: ^8.1.0
  equatable: ^2.0.5

  # Bluetooth
  flutter_blue_plus: ^1.31.0
  permission_handler: ^11.0.0

  # UI Components
  fl_chart: ^0.66.0

  # Utilities
  shared_preferences: ^2.2.0

  # Architecture
  dartz: ^0.10.1
  get_it: ^7.6.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
```

## AndroidManifest.xml 模板（蓝牙权限）

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.project_name">

    <!-- Bluetooth Permissions -->
    <uses-permission android:name="android.permission.BLUETOOTH"
        android:maxSdkVersion="30" />
    <uses-permission android:name="android.permission.BLUETOOTH_ADMIN"
        android:maxSdkVersion="30" />
    <uses-permission android:name="android.permission.BLUETOOTH_SCAN" />
    <uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />

    <!-- Location Permission (required for BLE scanning on Android) -->
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />

    <!-- Internet Permission (if needed) -->
    <uses-permission android:name="android.permission.INTERNET" />

    <application
        android:label="Project Name"
        android:icon="@mipmap/ic_launcher">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:theme="@style/LaunchTheme"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|smallestScreenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
            android:hardwareAccelerated="true"
            android:windowSoftInputMode="adjustResize">
            <meta-data
                android:name="io.flutter.embedding.android.NormalTheme"
                android:resource="@style/NormalTheme" />
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>
```

## Info.plist 模板（iOS 蓝牙权限）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSBluetoothAlwaysUsageDescription</key>
    <string>This app needs Bluetooth access to connect to devices.</string>
    <key>NSBluetoothPeripheralUsageDescription</key>
    <string>This app uses Bluetooth to connect to devices.</string>
    <key>NSLocationWhenInUseUsageDescription</key>
    <string>This app needs location access to discover Bluetooth devices.</string>
    <key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
    <string>This app needs location access to discover Bluetooth devices.</string>
</dict>
</plist>
```

## build.gradle 模板（APK 构建配置）

```gradle
android {
    compileSdkVersion 34

    defaultConfig {
        applicationId "com.example.project_name"
        minSdkVersion 21
        targetSdkVersion 34
        versionCode 1
        versionName "1.0.0"
    }

    buildTypes {
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
        debug {
            minifyEnabled false
        }
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'com.google.android.material:material:1.11.0'
}
```

## main.dart 模板（Riverpod + ProviderScope）

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const MainScreen(),
    );
  }
}

class MainScreen extends StatelessWidget {
  const MainScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Main Screen'),
      ),
      body: const Center(
        child: Text('Hello World'),
      ),
    );
  }
}
```

## main.dart 模板（BLoC + MaterialApp）

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:project_name/app/bloc/app_bloc.dart';
import 'package:project_name/app/bloc/app_event.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: BlocProvider(
        create: (context) => AppBloc(),
        child: const MainScreen(),
      ),
    );
  }
}
```
