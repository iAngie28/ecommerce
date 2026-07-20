import 'package:flutter/material.dart';

class StarRating extends StatelessWidget {
  final int rating;
  final Function(int)? onRatingChanged;
  final bool readOnly;
  final double size;

  const StarRating({
    Key? key,
    this.rating = 0,
    this.onRatingChanged,
    this.readOnly = true,
    this.size = 24.0,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: List.generate(5, (index) {
        final starValue = index + 1;
        final isActive = starValue <= rating;

        return GestureDetector(
          onTap: readOnly ? null : () => onRatingChanged?.call(starValue),
          child: Icon(
            isActive ? Icons.star : Icons.star_border,
            color: isActive ? Colors.amber : Colors.grey.shade400,
            size: size,
          ),
        );
      }),
    );
  }
}
