# Widget 模板

## Stateful Widget 模板

```dart
import 'package:flutter/material.dart';

class WidgetName extends StatefulWidget {
  final WidgetParameter parameter;

  const WidgetName({
    Key? key,
    required this.parameter,
  }) : super(key: key);

  @override
  State<WidgetName> createState() => _WidgetNameState();
}

class _WidgetNameState extends State<WidgetName> {
  // State variables
  late StreamSubscription _subscription;

  @override
  void initState() {
    super.initState();
    // Initialization
  }

  @override
  void dispose() {
    // Cleanup
    _subscription.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Widget Name')),
      body: _buildBody(context),
    );
  }

  Widget _buildBody(BuildContext context) {
    return const Center(
      child: Text('Hello World'),
    );
  }
}
```

## Riverpod Consumer Widget 模板

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class ConsumerWidgetName extends ConsumerWidget {
  const ConsumerWidgetName({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Watch provider
    final state = ref.watch(someProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Consumer Widget')),
      body: _buildBody(context, ref),
    );
  }

  Widget _buildBody(BuildContext context, WidgetRef ref) {
    return const Center(
      child: Text('Hello from Riverpod'),
    );
  }
}
```

## List Item 模板

```dart
import 'package:flutter/material.dart';

class ListItemWidget extends StatelessWidget {
  final ItemModel item;
  final VoidCallback onTap;
  final VoidCallback? onLongPress;

  const ListItemWidget({
    Key? key,
    required this.item,
    required this.onTap,
    this.onLongPress,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      child: ListTile(
        leading: _buildLeading(),
        title: _buildTitle(),
        subtitle: _buildSubtitle(),
        trailing: _buildTrailing(),
        onTap: onTap,
        onLongPress: onLongPress,
      ),
    );
  }

  Widget _buildLeading() {
    return const Icon(Icons.circle);
  }

  Widget _buildTitle() {
    return Text(item.title);
  }

  Widget _buildSubtitle() {
    return Text(item.subtitle);
  }

  Widget _buildTrailing() {
    return const Icon(Icons.chevron_right);
  }
}
```

## Loading Widget 模板

```dart
import 'package:flutter/material.dart';

class LoadingWidget extends StatelessWidget {
  final String? message;

  const LoadingWidget({Key? key, this.message}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const CircularProgressIndicator(),
          if (message != null) ...[
            const SizedBox(height: 16),
            Text(message!),
          ],
        ],
      ),
    );
  }
}
```

## Error Widget 模板

```dart
import 'package:flutter/material.dart';

class ErrorWidget extends StatelessWidget {
  final String message;
  final VoidCallback? onRetry;

  const ErrorWidget({
    Key? key,
    required this.message,
    this.onRetry,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.error_outline, size: 48, color: Colors.red),
            const SizedBox(height: 16),
            Text(
              message,
              textAlign: TextAlign.center,
              style: const TextStyle(color: Colors.red),
            ),
            if (onRetry != null) ...[
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: onRetry,
                child: const Text('Retry'),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
```

## Empty Widget 模板

```dart
import 'package:flutter/material.dart';

class EmptyWidget extends StatelessWidget {
  final String? message;
  final IconData? icon;

  const EmptyWidget({
    Key? key,
    this.message = 'No data available',
    this.icon = Icons.inbox,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon ?? Icons.inbox, size: 64, color: Colors.grey[400]),
          const SizedBox(height: 16),
          Text(
            message!,
            style: TextStyle(color: Colors.grey[600]),
          ),
        ],
      ),
    );
  }
}
```
