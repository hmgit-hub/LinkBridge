# LinkBridge Mobile App

LinkBridge 移动端应用，基于 Flutter 构建，支持 iOS 和 Android 平台。

## 项目结构

```
mobile/
├── lib/
│   ├── services/          # 服务层
│   │   ├── dio_service.dart         # Dio 网络请求封装
│   │   ├── hive_service.dart        # Hive 本地数据库
│   │   ├── auth_service.dart        # 认证服务
│   │   ├── link_service.dart        # 链接服务
│   │   └── notification_service.dart # 通知服务
│   ├── models/            # 数据模型
│   │   ├── file_item.dart          # 文件项模型
│   │   └── symlink_request.dart    # 软链接请求模型
│   ├── providers/          # Riverpod 状态管理
│   │   ├── file_list_provider.dart       # 文件列表状态
│   │   └── broken_symlinks_provider.dart # 断链状态
│   ├── screens/           # 页面
│   │   ├── dashboard_page.dart     # 链接列表页
│   │   ├── scan_page.dart          # 二维码扫描页
│   │   └── create_link_wizard.dart # 创建链接向导
│   ├── widgets/           # 组件
│   ├── utils/             # 工具类
│   └── main.dart          # 应用入口
├── android/               # Android 配置
│   └── app/src/main/AndroidManifest.xml
├── ios/                   # iOS 配置
│   └── Runner/Info.plist
├── pubspec.yaml           # 依赖配置
└── README.md              # 项目文档
```

## 核心功能

### 1. 链接列表 (DashboardPage)
- 展示所有软链接
- 区分正常/断链状态（红色高亮）
- 支持下拉刷新
- 支持无限滚动

### 2. 二维码扫描 (ScanPage)
- 集成 `mobile_scanner` 实现二维码扫描
- 解析 JSON 格式的路径信息
- 自动创建软链接

### 3. 创建链接向导 (CreateLinkWizard)
- 三步向导：选源 -> 选目标 -> 确认
- 支持从手机本地文件选择器选取
- 实时验证路径有效性

### 4. 断链通知
- 集成 `flutter_local_notifications` 实现断链报警
- 后台定时检查断链
- 推送通知提醒用户

### 5. 生物识别登录
- 集成 `local_auth` 实现指纹/FaceID 验证
- 保护应用安全

### 6. 离线优先
- 使用 `Hive` 本地数据库缓存目录列表
- 弱网下优先展示缓存
- 网络恢复后自动同步

## 技术栈

- **UI 框架**: Flutter 3.x
- **状态管理**: Riverpod 2.x
- **网络请求**: Dio 5.x
- **本地存储**: Hive 2.x
- **二维码扫描**: mobile_scanner 5.x
- **本地通知**: flutter_local_notifications 17.x
- **生物识别**: local_auth 2.x
- **文件选择**: file_picker 8.x

## 快速开始

### 环境要求

- Flutter SDK >= 3.0.0
- Dart SDK >= 3.0.0
- Android Studio / Xcode

### 安装依赖

```bash
flutter pub get
```

### 代码生成

```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

### 运行应用

```bash
# Android
flutter run

# iOS
flutter run
```

### 构建发布包

```bash
# Android APK
flutter build apk --release

# Android App Bundle
flutter build appbundle --release

# iOS
flutter build ios --release
```

## 权限配置

### Android (AndroidManifest.xml)

```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.CAMERA"/>
<uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.USE_BIOMETRIC"/>
<uses-permission android:name="android.permission.USE_FINGERPRINT"/>
```

### iOS (Info.plist)

```xml
<key>NSCameraUsageDescription</key>
<string>We need camera access to scan QR codes</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>We need photo library access to select files</string>
<key>NSFaceIDUsageDescription</key>
<string>We need FaceID access to authenticate users</string>
```

## API 接口

应用对接后端 API，接口地址可在 `dio_service.dart` 中配置：

```dart
BaseOptions(
  baseUrl: 'http://192.168.1.100:8000/api/v1',
  ...
)
```

## 注意事项

1. **代码生成**: 修改 `@riverpod` 注解的文件后，需要运行 `build_runner` 重新生成代码
2. **Hive 类型注册**: 新增 `@HiveType` 类型后，需要在 `main.dart` 中注册
3. **权限请求**: 首次使用相机、通知等功能时，会自动请求权限
4. **网络配置**: 确保手机与后端服务器在同一局域网

## 故障排查

### 代码生成失败

```bash
flutter clean
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
```

### iOS 构建失败

```bash
cd ios
pod install
cd ..
flutter clean
flutter pub get
flutter run
```

### Android 构建失败

```bash
cd android
./gradlew clean
cd ..
flutter clean
flutter pub get
flutter run
```
