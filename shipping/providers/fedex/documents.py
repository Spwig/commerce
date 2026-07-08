# -*- coding: utf-8 -*-
"""
FedEx Document Upload API Integration.

Supports uploading customs documents (commercial invoices, certificates of origin, etc.)
for international shipments using the FedEx Electronic Trade Documents (ETD) service.

Documentation: https://developer.fedex.com/api/en-us/catalog/upload-document/v1/docs.html

Workflows:
1. Pre-shipment: Upload docs → get docId → attach to shipment
2. Post-shipment: Create shipment → upload with tracking number
"""
import logging
import base64
from typing import Dict, List, Optional, Any
from decimal import Decimal

from .exceptions import (
    FedExError,
    FedExValidationError,
    FedExDocumentError,
)

logger = logging.getLogger(__name__)


class FedExDocumentUploader:
    """
    Handles document upload operations for FedEx Electronic Trade Documents (ETD).

    Supports:
    - Commercial invoices
    - Certificates of origin
    - USMCA certificates
    - Pro forma invoices
    - Other customs documents
    """

    # Supported document types
    DOCUMENT_TYPES = {
        'COMMERCIAL_INVOICE': 'Commercial Invoice',
        'CERTIFICATE_OF_ORIGIN': 'Certificate of Origin',
        'USMCA_CERTIFICATE_OF_ORIGIN': 'USMCA Certificate of Origin',
        'PRO_FORMA_INVOICE': 'Pro Forma Invoice',
        'OTHER': 'Other Document',
    }

    # File size limits (FedEx API limits)
    MAX_FILE_SIZE_MB = 5
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
    MAX_DOCUMENTS_PER_UPLOAD = 5

    def __init__(self, api_client):
        """
        Initialize document uploader.

        Args:
            api_client: FedExAPIClient instance for making API calls
        """
        self.api_client = api_client

    def upload_pre_shipment_document(
        self,
        document_type: str,
        file_content: bytes,
        file_name: str,
        reference_id: Optional[str] = None,
        workflow_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Upload a document before creating the shipment (pre-shipment workflow).

        Returns a document ID that can be attached to the shipment when creating the label.

        Args:
            document_type: Type of document (COMMERCIAL_INVOICE, CERTIFICATE_OF_ORIGIN, etc.)
            file_content: Binary file content
            file_name: Original filename (e.g., "invoice.pdf")
            reference_id: Optional reference ID for tracking
            workflow_name: Optional workflow name

        Returns:
            {
                'success': bool,
                'document_id': str,  # Use this when creating shipment
                'reference_id': str,
                'message': str,
            }

        Raises:
            FedExValidationError: If document validation fails
            FedExDocumentError: If upload fails
        """
        logger.info(f"Uploading pre-shipment document: {file_name} ({document_type})")

        # Validate document
        self._validate_document(document_type, file_content, file_name)

        # Encode file to base64
        encoded_content = base64.b64encode(file_content).decode('utf-8')

        # Build request payload
        payload = {
            'workflowName': workflow_name or 'ETDPostshipment',
            'carrierCode': 'FDXE',  # FedEx Express
            'documents': [{
                'contentType': self._get_content_type(file_name),
                'workflowName': workflow_name or 'ETDPostshipment',
                'documentType': document_type,
                'fileName': file_name,
                'documentContent': encoded_content,
            }]
        }

        if reference_id:
            payload['referenceId'] = reference_id

        try:
            # Make API request
            response = self.api_client._make_request(
                'POST',
                '/documents/v1/etds/upload',
                json=payload
            )

            # Extract document ID from response
            output = response.get('output', {})
            meta = output.get('meta', {})
            document_id = meta.get('documentId')

            if not document_id:
                raise FedExDocumentError("No document ID returned from upload")

            logger.info(f"Document uploaded successfully: {document_id}")

            return {
                'success': True,
                'document_id': document_id,
                'reference_id': reference_id or '',
                'message': f'Document {file_name} uploaded successfully',
            }

        except Exception as e:
            logger.error(f"Document upload failed: {e}")
            raise FedExDocumentError(f"Failed to upload document: {e}")

    def upload_post_shipment_document(
        self,
        tracking_number: str,
        document_type: str,
        file_content: bytes,
        file_name: str,
    ) -> Dict[str, Any]:
        """
        Upload a document after shipment creation (post-shipment workflow).

        Use this when you already have a tracking number and want to attach documents.

        Args:
            tracking_number: FedEx tracking number
            document_type: Type of document (COMMERCIAL_INVOICE, CERTIFICATE_OF_ORIGIN, etc.)
            file_content: Binary file content
            file_name: Original filename

        Returns:
            {
                'success': bool,
                'document_id': str,
                'tracking_number': str,
                'message': str,
            }

        Raises:
            FedExValidationError: If document validation fails
            FedExDocumentError: If upload fails
        """
        logger.info(f"Uploading post-shipment document for {tracking_number}: {file_name}")

        # Validate document
        self._validate_document(document_type, file_content, file_name)

        # Encode file to base64
        encoded_content = base64.b64encode(file_content).decode('utf-8')

        # Build request payload
        payload = {
            'workflowName': 'ETDPostshipment',
            'carrierCode': 'FDXE',
            'trackingNumber': tracking_number,
            'documents': [{
                'contentType': self._get_content_type(file_name),
                'workflowName': 'ETDPostshipment',
                'documentType': document_type,
                'fileName': file_name,
                'documentContent': encoded_content,
            }]
        }

        try:
            # Make API request
            response = self.api_client._make_request(
                'POST',
                '/documents/v1/etds/upload',
                json=payload
            )

            # Extract document ID from response
            output = response.get('output', {})
            meta = output.get('meta', {})
            document_id = meta.get('documentId')

            if not document_id:
                raise FedExDocumentError("No document ID returned from upload")

            logger.info(f"Post-shipment document uploaded: {document_id}")

            return {
                'success': True,
                'document_id': document_id,
                'tracking_number': tracking_number,
                'message': f'Document {file_name} attached to shipment {tracking_number}',
            }

        except Exception as e:
            logger.error(f"Post-shipment document upload failed: {e}")
            raise FedExDocumentError(f"Failed to upload post-shipment document: {e}")

    def generate_commercial_invoice_data(
        self,
        order_items: List[Dict[str, Any]],
        shipper: Dict[str, Any],
        recipient: Dict[str, Any],
        currency: str = 'USD',
    ) -> Dict[str, Any]:
        """
        Generate commercial invoice data structure for FedEx.

        Note: For MVP, we recommend using FedEx-generated documents instead of
        uploading custom PDFs. This method prepares the data structure that
        FedEx will use to generate the commercial invoice.

        Args:
            order_items: List of items with product, quantity, price, hs_code, etc.
            shipper: Shipper address and details
            recipient: Recipient address and details
            currency: ISO currency code (default: USD)

        Returns:
            Dict containing commercial invoice data ready for FedEx API
        """
        # Calculate totals
        subtotal = Decimal('0')
        total_weight = Decimal('0')

        commodities = []

        for item in order_items:
            product = item.get('product')
            quantity = item.get('quantity', 1)

            # Get customs data from product
            if not product.is_international_shipping_ready():
                missing = product.get_missing_customs_fields()
                raise FedExValidationError(
                    f"Product {product.name} missing customs data: {', '.join(missing)}"
                )

            unit_price = product.unit_price_for_customs
            total_price = unit_price * Decimal(str(quantity))
            subtotal += total_price

            # Add commodity
            commodities.append({
                'description': product.name[:35],  # FedEx limit
                'quantity': quantity,
                'unitPrice': {
                    'currency': currency,
                    'amount': float(unit_price),
                },
                'customsValue': {
                    'currency': currency,
                    'amount': float(total_price),
                },
                'weight': {
                    'units': 'LB',
                    'value': float(product.weight or 0),
                },
                'countryOfManufacture': product.country_of_origin,
                'harmonizedCode': product.hs_code,
                'exportLicenseNumber': product.export_license_number or None,
                'exportLicenseExpirationDate': (
                    product.export_license_expiry.isoformat()
                    if product.export_license_expiry else None
                ),
            })

            total_weight += Decimal(str(product.weight or 0)) * Decimal(str(quantity))

        return {
            'commodities': commodities,
            'shipper': shipper,
            'recipient': recipient,
            'totals': {
                'subtotal': float(subtotal),
                'currency': currency,
                'total_weight': float(total_weight),
            },
        }

    def _validate_document(
        self,
        document_type: str,
        file_content: bytes,
        file_name: str,
    ) -> None:
        """
        Validate document before upload.

        Raises:
            FedExValidationError: If validation fails
        """
        # Check document type
        if document_type not in self.DOCUMENT_TYPES:
            valid_types = ', '.join(self.DOCUMENT_TYPES.keys())
            raise FedExValidationError(
                f"Invalid document type: {document_type}. "
                f"Valid types: {valid_types}"
            )

        # Check file size
        file_size = len(file_content)
        if file_size > self.MAX_FILE_SIZE_BYTES:
            raise FedExValidationError(
                f"File size {file_size / 1024 / 1024:.2f}MB exceeds "
                f"maximum {self.MAX_FILE_SIZE_MB}MB"
            )

        # Check file extension
        allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg']
        file_ext = '.' + file_name.split('.')[-1].lower() if '.' in file_name else ''
        if file_ext not in allowed_extensions:
            raise FedExValidationError(
                f"Unsupported file type: {file_ext}. "
                f"Allowed: {', '.join(allowed_extensions)}"
            )

        logger.debug(f"Document validation passed: {file_name} ({file_size} bytes)")

    def _get_content_type(self, file_name: str) -> str:
        """
        Determine content type from file extension.

        Args:
            file_name: Original filename

        Returns:
            MIME type string
        """
        file_ext = '.' + file_name.split('.')[-1].lower() if '.' in file_name else ''

        content_types = {
            '.pdf': 'application/pdf',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
        }

        return content_types.get(file_ext, 'application/pdf')
