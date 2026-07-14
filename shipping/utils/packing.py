"""
Shipping Package Selection and Bin-Packing Algorithm

Automatically selects optimal shipping packages for cart items based on:
- Physical dimensions (length, width, height)
- Weight constraints
- Package priority
- Cost optimization

Supports both single-item and multi-item packing scenarios.
"""

import logging
from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from shipping.models import ShippingPackage

logger = logging.getLogger(__name__)


@dataclass
class PackableItem:
    """Represents an item to be packed"""

    id: str  # Unique identifier (e.g., "product_123" or "variant_456")
    name: str
    length: Decimal  # cm
    width: Decimal  # cm
    height: Decimal  # cm
    weight: Decimal  # kg
    quantity: int = 1
    fragile: bool = False

    def get_volume(self) -> Decimal:
        """Calculate item volume in cubic centimeters"""
        return self.length * self.width * self.height

    def get_dimensions_sorted(self) -> tuple[Decimal, Decimal, Decimal]:
        """Return dimensions sorted largest to smallest"""
        return tuple(sorted([self.length, self.width, self.height], reverse=True))


@dataclass
class PackingResult:
    """Result of packing operation"""

    package: "ShippingPackage"  # The selected package
    items: list[PackableItem]  # Items packed in this package
    total_weight: Decimal  # Total weight including package tare
    total_volume_used: Decimal  # Cubic cm used
    volume_utilization: Decimal  # Percentage of package volume used
    weight_utilization: Decimal  # Percentage of weight capacity used

    def __str__(self):
        return (
            f"Package: {self.package.name} | "
            f"Items: {len(self.items)} | "
            f"Weight: {self.total_weight}kg / {self.package.max_weight}kg "
            f"({self.weight_utilization:.1f}%) | "
            f"Volume: {self.volume_utilization:.1f}%"
        )


class PackingAlgorithm:
    """
    Sophisticated bin-packing algorithm for shipping package selection.

    Uses a greedy approach with volume and weight constraints:
    1. First-Fit Decreasing (FFD) for initial packing
    2. Weight validation
    3. Priority-based package selection
    4. Cost optimization
    """

    def __init__(self, available_packages: list["ShippingPackage"]):
        """
        Initialize packing algorithm with available packages.

        Args:
            available_packages: List of ShippingPackage instances to choose from
        """
        # Filter to active packages and sort by priority (desc) then volume (asc)
        self.packages = sorted(
            [p for p in available_packages if p.is_active],
            key=lambda p: (-p.priority, p.get_volume()),
        )

    def find_package_for_single_item(self, item: PackableItem) -> Optional["ShippingPackage"]:
        """
        Find the smallest package that fits a single item.

        Args:
            item: The item to pack

        Returns:
            ShippingPackage instance or None if no package fits
        """
        item_dims = item.get_dimensions_sorted()

        # Find all packages that can fit this item
        fitting_packages = []
        for package in self.packages:
            pkg_dims = sorted([package.length, package.width, package.height], reverse=True)

            # Check if item fits in any orientation
            if all(
                item_dim <= pkg_dim for item_dim, pkg_dim in zip(item_dims, pkg_dims, strict=True)
            ):
                # Check weight constraint
                if item.weight * item.quantity <= package.max_weight:
                    fitting_packages.append(package)

        if not fitting_packages:
            logger.warning(
                f"No package found for item {item.name} "
                f"(dimensions: {item.length}×{item.width}×{item.height}cm, "
                f"weight: {item.weight}kg)"
            )
            return None

        # Return smallest package by volume (already sorted)
        return fitting_packages[0]

    def pack_items(
        self,
        items: list[PackableItem],
        optimize_for: str = "cost",  # 'cost', 'volume', or 'count'
    ) -> list[PackingResult]:
        """
        Pack multiple items into optimal packages.

        Args:
            items: List of items to pack
            optimize_for: Optimization strategy:
                - 'cost': Minimize total shipping cost
                - 'volume': Maximize volume utilization
                - 'count': Minimize number of packages

        Returns:
            List of PackingResult instances
        """
        if not items:
            return []

        # Expand items by quantity (treat each quantity as separate item)
        expanded_items = []
        for item in items:
            for _ in range(item.quantity):
                # Create a copy with quantity=1
                single_item = PackableItem(
                    id=item.id,
                    name=item.name,
                    length=item.length,
                    width=item.width,
                    height=item.height,
                    weight=item.weight,
                    quantity=1,
                    fragile=item.fragile,
                )
                expanded_items.append(single_item)

        # Sort items by volume (largest first) - First-Fit Decreasing strategy
        sorted_items = sorted(expanded_items, key=lambda x: x.get_volume(), reverse=True)

        # Try to pack all items into packages
        packing_results = []
        remaining_items = sorted_items.copy()

        while remaining_items:
            # Try to pack as many items as possible into a single package
            best_packing = self._find_best_packing(remaining_items, optimize_for=optimize_for)

            if best_packing is None:
                # No package can fit even the largest remaining item
                logger.error(
                    f"Cannot pack item: {remaining_items[0].name} - no suitable package available"
                )
                break

            packing_results.append(best_packing)

            # Remove packed items from remaining items
            for packed_item in best_packing.items:
                remaining_items.remove(packed_item)

        return packing_results

    def _find_best_packing(
        self, items: list[PackableItem], optimize_for: str
    ) -> PackingResult | None:
        """
        Find the best package and item combination for packing.

        Args:
            items: Available items to pack (sorted largest first)
            optimize_for: Optimization strategy

        Returns:
            PackingResult or None if no valid packing exists
        """
        best_result = None
        best_score = float("inf")

        # Try each package
        for package in self.packages:
            # Try to fit as many items as possible into this package
            packed_items, total_weight, total_volume = self._pack_into_package(package, items)

            if not packed_items:
                continue  # No items fit in this package

            # Calculate utilization metrics
            volume_utilization = (total_volume / package.get_volume()) * 100
            weight_with_tare = total_weight + package.tare_weight
            weight_utilization = (weight_with_tare / package.max_weight) * 100

            # Create packing result
            result = PackingResult(
                package=package,
                items=packed_items,
                total_weight=weight_with_tare,
                total_volume_used=total_volume,
                volume_utilization=volume_utilization,
                weight_utilization=weight_utilization,
            )

            # Score this packing based on optimization strategy
            score = self._calculate_packing_score(result, optimize_for=optimize_for)

            # Keep best result
            if score < best_score:
                best_score = score
                best_result = result

        return best_result

    def _pack_into_package(
        self, package: "ShippingPackage", items: list[PackableItem]
    ) -> tuple[list[PackableItem], Decimal, Decimal]:
        """
        Greedy packing: fit as many items as possible into a package.

        This is a simplified 3D bin-packing implementation.
        For production use, consider more sophisticated algorithms like:
        - Guillotine algorithm
        - Maximal Rectangles
        - Shelf algorithms

        Args:
            package: Package to pack into
            items: Items to pack (sorted largest first)

        Returns:
            Tuple of (packed_items, total_weight, total_volume_used)
        """
        packed_items = []
        total_weight = Decimal("0.00")
        total_volume = Decimal("0.00")

        for item in items:
            # Check if item fits dimensionally
            if not package.fits_item(item.length, item.width, item.height):
                continue

            # Check if adding this item would exceed weight limit
            potential_weight = total_weight + item.weight
            if potential_weight > package.max_weight:
                continue

            # Check if volume would fit (simplified check)
            potential_volume = total_volume + item.get_volume()
            if potential_volume > package.get_volume():
                continue

            # Item fits! Add it
            packed_items.append(item)
            total_weight = potential_weight
            total_volume = potential_volume

        return packed_items, total_weight, total_volume

    def _calculate_packing_score(self, result: PackingResult, optimize_for: str) -> float:
        """
        Calculate a score for a packing result (lower is better).

        Args:
            result: PackingResult to score
            optimize_for: Optimization strategy

        Returns:
            Score (lower is better)
        """
        if optimize_for == "cost":
            # Minimize cost, prefer higher utilization
            cost_score = float(result.package.cost.amount if result.package.cost else 0)
            utilization_penalty = 100.0 - float(result.volume_utilization)
            return cost_score + (utilization_penalty * 0.01)

        elif optimize_for == "volume":
            # Maximize volume utilization (minimize unused space)
            return 100.0 - float(result.volume_utilization)

        else:  # optimize_for == 'count'
            # Minimize number of packages (pack most items per package)
            # Lower score for more items packed
            return -len(result.items)


def pack_cart_items(cart_items, optimize_for: str = "cost") -> list[PackingResult]:
    """
    Convenience function to pack cart items into shipping packages.

    Args:
        cart_items: QuerySet or list of CartItem instances
        optimize_for: Optimization strategy ('cost', 'volume', or 'count')

    Returns:
        List of PackingResult instances

    Example:
        >>> cart = Cart.objects.get(id=123)
        >>> packing_results = pack_cart_items(cart.items.all())
        >>> for result in packing_results:
        >>>     print(f"Package: {result.package.name}")
        >>>     print(f"Weight: {result.total_weight}kg")
        >>>     print(f"Items: {', '.join([item.name for item in result.items])}")
    """
    from shipping.models import ShippingPackage

    # Get all active shipping packages
    available_packages = ShippingPackage.objects.filter(is_active=True)

    if not available_packages.exists():
        logger.error("No active shipping packages available for packing")
        return []

    # Convert cart items to PackableItem instances
    packable_items = []
    for cart_item in cart_items:
        # Determine which object has dimensions (variant or product)
        if cart_item.variant:
            source = cart_item.variant
            weight = source.get_effective_weight()
            dims = source.get_effective_dimensions()
        else:
            source = cart_item.product
            weight = source.weight
            dims = {"length": source.length, "width": source.width, "height": source.height}

        # Skip items without dimensions or weight
        if not all([dims["length"], dims["width"], dims["height"], weight]):
            logger.warning(f"Skipping cart item {cart_item.id}: missing dimensions or weight")
            continue

        packable_item = PackableItem(
            id=f"{cart_item.id}",
            name=cart_item.product.name,
            length=dims["length"],
            width=dims["width"],
            height=dims["height"],
            weight=weight,
            quantity=cart_item.quantity,
            fragile=False,  # Could be added to Product model in future
        )
        packable_items.append(packable_item)

    if not packable_items:
        logger.warning("No packable items found in cart")
        return []

    # Run packing algorithm
    algorithm = PackingAlgorithm(list(available_packages))
    return algorithm.pack_items(packable_items, optimize_for=optimize_for)
