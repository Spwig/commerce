(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var widget = document.querySelector('.attribute-selector-widget');
        var addToCartBtn = document.getElementById('add-to-cart-btn');

        if (widget && widget.attributeSelector) {
            var selector = widget.attributeSelector;

            // Example: Pass variants data to the widget
            // In a real implementation, this would come from your API
            var exampleVariants = [
                {
                    id: 1,
                    name: 'Red - Small',
                    sku: 'PROD-001-RED-SM',
                    attributes_structured: [
                        { id: 1, value: 'Red', attribute_name: 'Color' },
                        { id: 3, value: 'Small', attribute_name: 'Size' }
                    ],
                    effective_price: { amount: '99.99', currency: 'USD' },
                    stock_quantity: 10
                },
                {
                    id: 2,
                    name: 'Blue - Medium',
                    sku: 'PROD-001-BLUE-MD',
                    attributes_structured: [
                        { id: 2, value: 'Blue', attribute_name: 'Color' },
                        { id: 4, value: 'Medium', attribute_name: 'Size' }
                    ],
                    effective_price: { amount: '99.99', currency: 'USD' },
                    stock_quantity: 5
                }
            ];

            // Set variants
            selector.setVariants(exampleVariants);

            // Listen for variant changes
            widget.addEventListener('variantChange', function (e) {
                var variant = e.detail.variant;
                console.log('Variant selected:', variant);

                // Enable add to cart button
                addToCartBtn.disabled = false;
            });

            // Add to cart validation
            addToCartBtn.addEventListener('click', function () {
                var validation = selector.validate();

                if (!validation.valid) {
                    AdminModal.alert({message: 'Please select all required options:\n' + validation.errors.join('\n'), type: 'warning'});
                    return;
                }

                var selectedVariant = selector.getSelectedVariant();
                if (selectedVariant) {
                    AdminModal.toast('Added to cart: ' + selectedVariant.name + ' (' + selectedVariant.sku + ')', 'success');
                }
            });
        }
    });
})();
