import 'package:flutter/material.dart';
import '../services/wishlist_service.dart';

class WishlistButton extends StatefulWidget {
  final int productoId;
  final String token;
  final double size;

  const WishlistButton({
    Key? key,
    required this.productoId,
    required this.token,
    this.size = 28.0,
  }) : super(key: key);

  @override
  State<WishlistButton> createState() => _WishlistButtonState();
}

class _WishlistButtonState extends State<WishlistButton> with SingleTickerProviderStateMixin {
  final WishlistService _wishlistService = WishlistService();
  bool _enWishlist = false;
  bool _cargando = true;

  late AnimationController _animationController;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 200),
    );
    _scaleAnimation = TweenSequence<double>([
      TweenSequenceItem(tween: Tween(begin: 1.0, end: 1.3), weight: 50),
      TweenSequenceItem(tween: Tween(begin: 1.3, end: 1.0), weight: 50),
    ]).animate(_animationController);

    _verificarEstado();
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  Future<void> _verificarEstado() async {
    try {
      final status = await _wishlistService.verificarSiContiene(widget.productoId, widget.token);
      if (mounted) {
        setState(() {
          _enWishlist = status;
          _cargando = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() => _cargando = false);
      }
    }
  }

  Future<void> _toggleWishlist() async {
    if (_cargando) return;

    // Optimistic Update
    setState(() {
      _enWishlist = !_enWishlist;
    });
    
    if (_enWishlist) {
      _animationController.forward(from: 0.0);
    }

    try {
      await _wishlistService.toggleProducto(widget.productoId, widget.token);
    } catch (e) {
      // Revert if failed
      if (mounted) {
        setState(() {
          _enWishlist = !_enWishlist;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Error al actualizar lista de deseos')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_cargando) {
      return SizedBox(
        width: widget.size,
        height: widget.size,
        child: const Padding(
          padding: EdgeInsets.all(4.0),
          child: CircularProgressIndicator(strokeWidth: 2),
        ),
      );
    }

    return GestureDetector(
      onTap: _toggleWishlist,
      child: AnimatedBuilder(
        animation: _scaleAnimation,
        builder: (context, child) {
          return Transform.scale(
            scale: _scaleAnimation.value,
            child: Icon(
              _enWishlist ? Icons.favorite : Icons.favorite_border,
              color: _enWishlist ? Colors.red : Colors.grey,
              size: widget.size,
            ),
          );
        },
      ),
    );
  }
}
