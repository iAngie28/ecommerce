import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';
import '../../core/widgets/buttons/app_button.dart';
import '../../dashboard/models/product_model.dart';
import '../../dashboard/repositories/product_repository.dart';
import '../models/category_model.dart';

class ProductFormScreen extends StatefulWidget {
  final ProductModel? product;

  const ProductFormScreen({super.key, this.product});

  @override
  State<ProductFormScreen> createState() => _ProductFormScreenState();
}

class _ProductFormScreenState extends State<ProductFormScreen> {
  final _formKey = GlobalKey<FormState>();
  final ProductRepository _productRepository = ProductRepository();

  late TextEditingController _nameController;
  late TextEditingController _descController;
  late TextEditingController _priceController;
  late TextEditingController _stockController;
  late TextEditingController _skuController;

  List<CategoryModel> _categories = [];
  int? _selectedCategoryId;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController(text: widget.product?.nombre ?? '');
    _descController = TextEditingController(text: widget.product?.descripcion ?? '');
    _priceController = TextEditingController(text: widget.product?.precio.toString() ?? '');
    _stockController = TextEditingController(text: widget.product?.stock.toString() ?? '');
    _skuController = TextEditingController(text: widget.product?.sku ?? '');
    _selectedCategoryId = widget.product?.categoria;
    _loadCategories();
  }

  Future<void> _loadCategories() async {
    try {
      final cats = await _productRepository.fetchCategories();
      setState(() => _categories = cats);
    } catch (e) {
      debugPrint('Error loading categories: $e');
    }
  }

  Future<void> _save() async {
    if (!_formKey.currentState!.validate()) return;

    if (_selectedCategoryId == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Por favor, selecciona una categoría'), backgroundColor: AppColors.danger),
      );
      return;
    }

    setState(() => _isLoading = true);

    try {
      final productData = ProductModel(
        id: widget.product?.id ?? 0,
        nombre: _nameController.text,
        descripcion: _descController.text,
        precio: double.parse(_priceController.text),
        stock: int.parse(_stockController.text),
        sku: _skuController.text,
        categoria: _selectedCategoryId,
      );

      if (widget.product == null) {
        await _productRepository.createProduct(productData);
      } else {
        await _productRepository.updateProduct(widget.product!.id, productData);
      }

      if (mounted) Navigator.pop(context, true);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e'), backgroundColor: AppColors.danger),
      );
    } finally {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _showAddCategoryDialog() async {
    final nameController = TextEditingController();
    final result = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Nueva Categoría'),
        content: TextField(
          controller: nameController,
          style: const TextStyle(color: AppColors.textPrimary),
          decoration: const InputDecoration(labelText: 'Nombre de la categoría', hintText: 'Ej: Electrónica'),
          autofocus: true,
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Cancelar')),
          AppButton.primary(
            label: 'Crear',
            onPressed: () => Navigator.pop(context, true),
          ),
        ],
      ),
    );

    if (result == true && nameController.text.isNotEmpty) {
      try {
        final newCat = CategoryModel(id: 0, nombre: nameController.text, descripcion: '');
        await _productRepository.createCategory(newCat);
        await _loadCategories();
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final isEdit = widget.product != null;
    final orientation = MediaQuery.of(context).orientation;
    final isLandscape = orientation == Orientation.landscape;

    return Scaffold(
      appBar: AppBar(
        title: Text(isEdit ? 'Editar Producto' : 'Nuevo Producto', style: const TextStyle(color: AppColors.primaryDark)),
        backgroundColor: AppColors.white,
        elevation: 0,
        iconTheme: const IconThemeData(color: AppColors.primaryDark),
      ),
      backgroundColor: AppColors.bgLight,
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              if (isLandscape)
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Expanded(child: _buildField('Nombre del Producto', _nameController, Icons.shopping_bag)),
                    const SizedBox(width: 15),
                    Expanded(child: _buildField('SKU / Código', _skuController, Icons.qr_code)),
                  ],
                )
              else ...[
                _buildField('Nombre del Producto', _nameController, Icons.shopping_bag),
                const SizedBox(height: 15),
                _buildField('SKU / Código', _skuController, Icons.qr_code),
              ],
              const SizedBox(height: 15),
              _buildCategoryDropdown(),
              const SizedBox(height: 15),
              Row(
                children: [
                  Expanded(child: _buildField('Precio (BS.)', _priceController, Icons.attach_money, isNumber: true)),
                  const SizedBox(width: 15),
                  Expanded(child: _buildField('Stock Inicial', _stockController, Icons.inventory, isNumber: true)),
                ],
              ),
              const SizedBox(height: 15),
              _buildField('Descripción', _descController, Icons.description, maxLines: 3),
              const SizedBox(height: 30),
              AppButton.submit(
                label: _isLoading ? 'Guardando...' : (isEdit ? 'Actualizar Producto' : 'Crear Producto'),
                onPressed: _isLoading ? null : _save,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildField(String label, TextEditingController controller, IconData icon, {bool isNumber = false, int maxLines = 1}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
        const SizedBox(height: 8),
        TextFormField(
          controller: controller,
          keyboardType: isNumber ? TextInputType.number : TextInputType.text,
          maxLines: maxLines,
          style: const TextStyle(color: AppColors.textPrimary),
          decoration: InputDecoration(
            prefixIcon: Icon(icon, color: AppColors.accentTeal, size: 20),
            filled: true,
            fillColor: AppColors.white,
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide.none),
            contentPadding: const EdgeInsets.symmetric(horizontal: 15, vertical: 15),
          ),
          validator: (v) => (v == null || v.isEmpty) ? 'Campo requerido' : null,
        ),
      ],
    );
  }

  Widget _buildCategoryDropdown() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Categoría', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
        const SizedBox(height: 8),
        Row(
          children: [
            Expanded(
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 15),
                decoration: BoxDecoration(color: AppColors.white, borderRadius: BorderRadius.circular(10)),
                child: DropdownButtonHideUnderline(
                  child: DropdownButton<int>(
                    isExpanded: true,
                    value: _selectedCategoryId,
                    hint: const Text('Seleccionar categoría'),
                    items: _categories.map((cat) {
                      return DropdownMenuItem(value: cat.id, child: Text(cat.rutaCompleta ?? cat.nombre));
                    }).toList(),
                    onChanged: (v) => setState(() => _selectedCategoryId = v),
                  ),
                ),
              ),
            ),
            const SizedBox(width: 10),
            IconButton(
              onPressed: _showAddCategoryDialog,
              icon: const Icon(Icons.add_circle, color: AppColors.accentTeal, size: 30),
              tooltip: 'Nueva Categoría',
            ),
          ],
        ),
      ],
    );
  }
}
