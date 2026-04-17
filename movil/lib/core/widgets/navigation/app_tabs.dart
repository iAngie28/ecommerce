import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_radius.dart';

class AppTabs extends StatefulWidget {
  final List<String> tabs;
  final ValueChanged<int> onTabChanged;

  const AppTabs({
    super.key,
    required this.tabs,
    required this.onTabChanged,
  });

  @override
  State<AppTabs> createState() => _AppTabsState();
}

class _AppTabsState extends State<AppTabs> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(4),
      decoration: BoxDecoration(
        color: AppColors.bgSearch,
        borderRadius: BorderRadius.circular(AppRadius.md),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: List.generate(widget.tabs.length, (index) {
          final isSelected = _selectedIndex == index;
          return GestureDetector(
            onTap: () {
              setState(() => _selectedIndex = index);
              widget.onTabChanged(index);
            },
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
              decoration: BoxDecoration(
                color: isSelected ? AppColors.white : Colors.transparent,
                borderRadius: BorderRadius.circular(AppRadius.sm - 2),
                boxShadow: isSelected
                    ? [const BoxShadow(color: Colors.black12, blurRadius: 4, offset: Offset(0, 2))]
                    : [],
              ),
              child: Text(
                widget.tabs[index],
                style: TextStyle(
                  fontWeight: isSelected ? FontWeight.w600 : FontWeight.w500,
                  color: isSelected ? AppColors.primaryDark : AppColors.textSlate,
                ),
              ),
            ),
          );
        }),
      ),
    );
  }
}