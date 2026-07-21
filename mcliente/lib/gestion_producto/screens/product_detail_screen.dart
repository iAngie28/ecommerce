import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_text_styles.dart';
import '../../core/widgets/buttons/app_button.dart';
import '../../core/widgets/feedback/app_toast.dart';
import '../models/product_model.dart';
import '../models/review_model.dart';
import '../repositories/cart_repository.dart';
import '../repositories/review_repository.dart';
import '../repositories/wishlist_repository.dart';

class ProductDetailScreen extends StatefulWidget {
  final ProductModel product;

  const ProductDetailScreen({super.key, required this.product});

  @override
  State<ProductDetailScreen> createState() => _ProductDetailScreenState();
}

class _ProductDetailScreenState extends State<ProductDetailScreen> {
  final CartRepository _cartRepository = CartRepository();
  final WishlistRepository _wishlistRepository = WishlistRepository();
  final ReviewRepository _reviewRepository = ReviewRepository();
  final TextEditingController _reviewController = TextEditingController();
  late ProductModel _product;
  List<ReviewModel> _reviews = [];
  bool _isAdding = false;
  bool _isWishlistLoading = true;
  bool _isWishlistUpdating = false;
  bool _isReviewsLoading = false;
  bool _isReviewSubmitting = false;
  bool _reviewsChanged = false;
  bool _enWishlist = false;
  int _selectedRating = 0;

  @override
  void initState() {
    super.initState();
    _product = widget.product;
    _loadWishlistStatus();
    _loadReviews();
  }

  @override
  void dispose() {
    _reviewController.dispose();
    super.dispose();
  }

  Future<void> _loadWishlistStatus() async {
    try {
      final enWishlist = await _wishlistRepository.containsProduct(
        _product.id,
      );
      if (!mounted) return;
      setState(() {
        _enWishlist = enWishlist;
        _isWishlistLoading = false;
      });
    } catch (_) {
      if (!mounted) return;
      setState(() => _isWishlistLoading = false);
    }
  }

  Future<void> _toggleWishlist() async {
    if (_isWishlistUpdating) return;

    final previous = _enWishlist;
    setState(() {
      _isWishlistUpdating = true;
      _enWishlist = !previous;
    });

    try {
      final isSaved = await _wishlistRepository.toggleProduct(
        _product.id,
      );
      if (!mounted) return;
      setState(() {
        _enWishlist = isSaved;
        _isWishlistUpdating = false;
      });
      AppToast.showSuccess(
        context,
        isSaved
            ? 'Producto guardado en wishlist'
            : 'Producto quitado de wishlist',
      );
    } catch (_) {
      if (!mounted) return;
      setState(() {
        _enWishlist = previous;
        _isWishlistUpdating = false;
      });
      AppToast.showError(context, 'No se pudo actualizar la wishlist');
    }
  }

  Future<void> _addToCart() async {
    if (!_product.activo || _product.stock <= 0) {
      AppToast.showInfo(context, 'Producto no disponible');
      return;
    }

    setState(() => _isAdding = true);
    try {
      final cart = await _cartRepository.fetchActiveCart();
      await _cartRepository.addItem(cart.id, _product.id);
      if (!mounted) return;
      AppToast.showSuccess(context, '¡${_product.nombre} añadido!');
      _closeDetail(cartChanged: true);
    } catch (e) {
      if (!mounted) return;
      AppToast.showError(context, 'Error al añadir al carrito');
    } finally {
      if (mounted) setState(() => _isAdding = false);
    }
  }

  Future<void> _loadReviews() async {
    setState(() => _isReviewsLoading = true);

    try {
      final result = await _reviewRepository.fetchProductReviews(_product.id);
      if (!mounted) return;
      setState(() {
        _reviews = result.reviews;
        _isReviewsLoading = false;
        _product = _product.copyWith(
          promedioCalificacion: result.promedio,
          totalResenas: result.totalResenas,
        );
      });
    } catch (_) {
      if (!mounted) return;
      setState(() => _isReviewsLoading = false);
      AppToast.showError(context, 'No se pudieron cargar las reseñas');
    }
  }

  Future<void> _submitReview() async {
    if (_selectedRating == 0 || _isReviewSubmitting) {
      AppToast.showError(context, 'Por favor selecciona una calificación');
      return;
    }

    setState(() => _isReviewSubmitting = true);

    try {
      await _reviewRepository.submitReview(
        productId: _product.id,
        calificacion: _selectedRating,
        comentario: _reviewController.text.trim(),
      );
      if (!mounted) return;

      final newTotal = _product.totalResenas + 1;
      final newAverage =
          ((_product.promedioCalificacion * _product.totalResenas) +
              _selectedRating) /
          newTotal;

      setState(() {
        _selectedRating = 0;
        _reviewsChanged = true;
        _product = _product.copyWith(
          totalResenas: newTotal,
          promedioCalificacion: double.parse(newAverage.toStringAsFixed(1)),
        );
      });
      _reviewController.clear();
      AppToast.showSuccess(context, '¡Reseña enviada con éxito!');
      await _loadReviews();
    } catch (e) {
      if (!mounted) return;
      AppToast.showError(
        context,
        e.toString().replaceFirst('Exception: ', ''),
      );
    } finally {
      if (mounted) setState(() => _isReviewSubmitting = false);
    }
  }

  void _closeDetail({bool cartChanged = false}) {
    Navigator.pop(context, {
      'cartChanged': cartChanged,
      'reviewsChanged': _reviewsChanged,
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: CustomScrollView(
        slivers: [
          _buildAppBar(context),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildHeader(),
                  const SizedBox(height: 24),
                  _buildPriceSection(),
                  const SizedBox(height: 24),
                  _buildDescription(),
                  const SizedBox(height: 32),
                  _buildMetaInfo(),
                  const SizedBox(height: 32),
                  _buildReviewsSection(),
                  const SizedBox(height: 40),
                ],
              ),
            ),
          ),
        ],
      ),
      bottomNavigationBar: _buildBottomAction(),
    );
  }

  Widget _buildAppBar(BuildContext context) {
    return SliverAppBar(
      expandedHeight: 400,
      pinned: true,
      backgroundColor: AppColors.primaryDark,
      leading: IconButton(
        icon: const Icon(Icons.arrow_back, color: Colors.white),
        onPressed: () => _closeDetail(),
      ),
      actions: [
        IconButton(
          tooltip: _enWishlist ? 'Quitar de wishlist' : 'Guardar en wishlist',
          onPressed: _isWishlistLoading || _isWishlistUpdating
              ? null
              : _toggleWishlist,
          icon: _isWishlistLoading || _isWishlistUpdating
              ? const SizedBox(
                  width: 22,
                  height: 22,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    color: Colors.white,
                  ),
                )
              : Icon(
                  _enWishlist ? Icons.favorite : Icons.favorite_border,
                  color: _enWishlist ? AppColors.danger : Colors.white,
                ),
        ),
      ],
      flexibleSpace: FlexibleSpaceBar(
        background: Hero(
          tag: 'product-${_product.id}',
          child: Container(
            color: AppColors.bgSearch,
            child:
                _product.imagenUrl != null && _product.imagenUrl!.isNotEmpty
                ? Image.network(_product.imagenUrl!, fit: BoxFit.cover)
                : const Center(
                    child: Icon(
                      Icons.image_outlined,
                      size: 100,
                      color: AppColors.textMuted,
                    ),
                  ),
          ),
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
          decoration: BoxDecoration(
            color: AppColors.accentTeal.withOpacity(0.1),
            borderRadius: BorderRadius.circular(20),
          ),
          child: Text(
            _product.categoriaNombre?.toUpperCase() ?? 'GENERAL',
            style: const TextStyle(
              color: AppColors.accentTeal,
              fontWeight: FontWeight.bold,
              fontSize: 12,
              letterSpacing: 1.2,
            ),
          ),
        ),
        const SizedBox(height: 12),
        Text(_product.nombre, style: AppTextStyles.h1),
        const SizedBox(height: 12),
        _buildRatingBadge(_product.promedioCalificacion, _product.totalResenas),
      ],
    );
  }

  Widget _buildPriceSection() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Precio total',
              style: TextStyle(color: AppColors.textMuted, fontSize: 14),
            ),
            const SizedBox(height: 4),
            Text(
              'BS. ${_product.precio}',
              style: const TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.w900,
                color: AppColors.primaryDark,
                letterSpacing: -1,
              ),
            ),
          ],
        ),
        if (_product.stock < 5 && _product.stock > 0)
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: AppColors.danger.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: const Text(
              '🔥 ¡Pocas unidades!',
              style: TextStyle(
                color: AppColors.danger,
                fontWeight: FontWeight.bold,
                fontSize: 12,
              ),
            ),
          ),
      ],
    );
  }

  Widget _buildDescription() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Descripción', style: AppTextStyles.h3),
        const SizedBox(height: 12),
        Text(
          _product.descripcion.isNotEmpty
              ? _product.descripcion
              : 'Este producto no cuenta con una descripción detallada en este momento.',
          style: const TextStyle(
            fontSize: 16,
            color: AppColors.textPrimary,
            height: 1.6,
          ),
        ),
      ],
    );
  }

  Widget _buildMetaInfo() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.bgSearch,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Column(
        children: [
          _buildMetaRow(
            'Disponibilidad',
            _product.stock > 0
                ? '${_product.stock} unidades'
                : 'Agotado',
            _product.stock > 0 ? AppColors.accentTeal : AppColors.danger,
          ),
          const Divider(height: 30),
          _buildMetaRow(
            'Código SKU',
            _product.sku.isNotEmpty
                ? _product.sku
                : '#PRD-${_product.id}',
            AppColors.textPrimary,
          ),
        ],
      ),
    );
  }

  Widget _buildMetaRow(String label, String value, Color valueColor) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(label, style: const TextStyle(color: AppColors.textMuted)),
        Text(
          value,
          style: TextStyle(fontWeight: FontWeight.bold, color: valueColor),
        ),
      ],
    );
  }

  Widget _buildReviewsSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text('Reseñas', style: AppTextStyles.h3),
            _buildRatingBadge(
              _product.promedioCalificacion,
              _product.totalResenas,
              compact: true,
            ),
          ],
        ),
        const SizedBox(height: 16),
        _buildReviewForm(),
        const SizedBox(height: 20),
        if (_isReviewsLoading)
          const Center(
            child: Padding(
              padding: EdgeInsets.symmetric(vertical: 24),
              child: CircularProgressIndicator(color: AppColors.accentTeal),
            ),
          )
        else if (_reviews.isEmpty)
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(18),
            decoration: BoxDecoration(
              color: AppColors.bgSearch,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: AppColors.border),
            ),
            child: const Text(
              'Aún no hay reseñas para este producto.',
              textAlign: TextAlign.center,
              style: TextStyle(color: AppColors.textMuted),
            ),
          )
        else
          Column(
            children: _reviews
                .map(
                  (review) => Padding(
                    padding: const EdgeInsets.only(bottom: 12),
                    child: _buildReviewItem(review),
                  ),
                )
                .toList(),
          ),
      ],
    );
  }

  Widget _buildReviewForm() {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: AppColors.bgSearch,
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: AppColors.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Deja tu reseña',
            style: TextStyle(
              fontWeight: FontWeight.w800,
              fontSize: 16,
              color: AppColors.primaryDark,
            ),
          ),
          const SizedBox(height: 12),
          Row(
            children: List.generate(5, (index) {
              final rating = index + 1;
              return IconButton(
                tooltip: '$rating estrellas',
                padding: EdgeInsets.zero,
                constraints: const BoxConstraints(
                  minWidth: 36,
                  minHeight: 36,
                ),
                onPressed: _isReviewSubmitting
                    ? null
                    : () => setState(() => _selectedRating = rating),
                icon: Icon(
                  _selectedRating >= rating ? Icons.star : Icons.star_border,
                  color: AppColors.warning,
                  size: 30,
                ),
              );
            }),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _reviewController,
            maxLength: 1000,
            maxLines: 4,
            enabled: !_isReviewSubmitting,
            decoration: InputDecoration(
              hintText: 'Cuéntanos qué te pareció este producto...',
              filled: true,
              fillColor: Colors.white,
              counterStyle: const TextStyle(color: AppColors.textMuted),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(14),
                borderSide: const BorderSide(color: AppColors.border),
              ),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(14),
                borderSide: const BorderSide(color: AppColors.border),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(14),
                borderSide: const BorderSide(color: AppColors.accentTeal),
              ),
            ),
          ),
          const SizedBox(height: 8),
          AppButton.primary(
            label: _isReviewSubmitting ? 'Enviando...' : 'Enviar reseña',
            isLoading: _isReviewSubmitting,
            fullWidth: true,
            onPressed: _selectedRating > 0 ? _submitReview : null,
          ),
        ],
      ),
    );
  }

  Widget _buildReviewItem(ReviewModel review) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      review.clienteNombre,
                      style: const TextStyle(
                        fontWeight: FontWeight.w800,
                        color: AppColors.primaryDark,
                      ),
                    ),
                    const SizedBox(height: 4),
                    _buildReadOnlyStars(review.calificacion.toDouble()),
                  ],
                ),
              ),
              Text(
                _formatDate(review.fechaCreacion),
                style: const TextStyle(
                  color: AppColors.textMuted,
                  fontSize: 12,
                ),
              ),
            ],
          ),
          if (review.comentario.trim().isNotEmpty) ...[
            const SizedBox(height: 12),
            Text(
              review.comentario,
              style: const TextStyle(
                color: AppColors.textPrimary,
                height: 1.45,
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildRatingBadge(
    double rating,
    int total, {
    bool compact = false,
  }) {
    return Container(
      padding: EdgeInsets.symmetric(
        horizontal: compact ? 10 : 12,
        vertical: compact ? 6 : 8,
      ),
      decoration: BoxDecoration(
        color: AppColors.warningBg,
        borderRadius: BorderRadius.circular(999),
        border: Border.all(color: AppColors.warning.withValues(alpha: 0.25)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          _buildReadOnlyStars(rating, size: compact ? 14 : 16),
          const SizedBox(width: 6),
          Text(
            '($total)',
            style: TextStyle(
              color: AppColors.warningText,
              fontWeight: FontWeight.w800,
              fontSize: compact ? 12 : 13,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildReadOnlyStars(double rating, {double size = 14}) {
    final fullStars = rating.floor();
    final hasHalfStar = rating - fullStars >= 0.5;

    return Row(
      mainAxisSize: MainAxisSize.min,
      children: List.generate(5, (index) {
        IconData icon;
        if (index < fullStars) {
          icon = Icons.star;
        } else if (index == fullStars && hasHalfStar) {
          icon = Icons.star_half;
        } else {
          icon = Icons.star_border;
        }

        return Icon(icon, color: AppColors.warning, size: size);
      }),
    );
  }

  String _formatDate(DateTime? value) {
    if (value == null) return '';
    final local = value.toLocal();
    final day = local.day.toString().padLeft(2, '0');
    final month = local.month.toString().padLeft(2, '0');
    return '$day/$month/${local.year}';
  }

  Widget _buildBottomAction() {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, -5),
          ),
        ],
      ),
      child: AppButton.primary(
        label: _isAdding ? 'Añadiendo...' : 'Agregar al carrito',
        onPressed: _product.activo && _product.stock > 0 ? _addToCart : null,
      ),
    );
  }
}
