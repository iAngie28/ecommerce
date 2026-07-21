import 'package:flutter/foundation.dart';

class NotificationBadgeService {
  NotificationBadgeService._();

  static final ValueNotifier<int> pulse = ValueNotifier<int>(0);

  static void notifyChanged() {
    pulse.value++;
  }
}
