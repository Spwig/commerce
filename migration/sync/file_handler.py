"""
File Handler

Handles FileField/ImageField export (base64 encoding) and import for settings sync.
For small files like logos, favicons, and preview images.
For large media files, use media_transfer.py instead.
"""
import base64
import logging
import mimetypes
import os

from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)

# Maximum file size for inline base64 transfer (10MB)
MAX_INLINE_FILE_SIZE = 10 * 1024 * 1024


def export_file_field(instance, field_name):
    """
    Export a FileField/ImageField value as base64-encoded data.

    Args:
        instance: Model instance
        field_name: Name of the FileField/ImageField

    Returns:
        dict: {
            'filename': str,
            'content_type': str,
            'data': str (base64),
            'size': int,
        } or None if field is empty
    """
    field_file = getattr(instance, field_name, None)
    if not field_file or not field_file.name:
        return None

    try:
        # Check file size
        try:
            file_size = field_file.size
        except Exception:
            file_size = 0

        if file_size > MAX_INLINE_FILE_SIZE:
            logger.warning(
                f"File too large for inline transfer: {field_file.name} "
                f"({file_size} bytes > {MAX_INLINE_FILE_SIZE})"
            )
            return None

        # Read and encode
        field_file.open('rb')
        try:
            content = field_file.read()
        finally:
            field_file.close()

        content_type = mimetypes.guess_type(field_file.name)[0] or 'application/octet-stream'

        return {
            'filename': field_file.name,
            'content_type': content_type,
            'data': base64.b64encode(content).decode('ascii'),
            'size': len(content),
        }

    except Exception as e:
        logger.error(f"Failed to export file {field_name} from {instance}: {e}")
        return None


def import_file_field(instance, field_name, file_data):
    """
    Import a base64-encoded file into a FileField/ImageField.

    Args:
        instance: Model instance
        field_name: Name of the FileField/ImageField
        file_data: dict from export_file_field()

    Returns:
        bool: True if import was successful
    """
    if not file_data or not file_data.get('data'):
        return False

    try:
        content = base64.b64decode(file_data['data'])
        filename = file_data.get('filename', 'imported_file')

        # Extract just the filename (not the full path) to let Django handle upload_to
        filename = os.path.basename(filename)

        content_file = ContentFile(content, name=filename)
        field = getattr(instance, field_name)
        field.save(filename, content_file, save=False)

        return True

    except Exception as e:
        logger.error(f"Failed to import file {field_name} to {instance}: {e}")
        return False


def export_model_files(instance, file_fields):
    """
    Export all file fields from a model instance.

    Args:
        instance: Model instance
        file_fields: list of field names that are FileField/ImageField

    Returns:
        dict: field_name -> file_data dict
    """
    files = {}
    for field_name in file_fields:
        file_data = export_file_field(instance, field_name)
        if file_data:
            files[field_name] = file_data
    return files


def import_model_files(instance, files_data, file_fields):
    """
    Import all file fields into a model instance.

    Args:
        instance: Model instance
        files_data: dict of field_name -> file_data from export
        file_fields: list of field names to import

    Returns:
        dict: {imported: int, failed: int}
    """
    imported = 0
    failed = 0

    for field_name in file_fields:
        file_data = files_data.get(field_name)
        if file_data:
            if import_file_field(instance, field_name, file_data):
                imported += 1
            else:
                failed += 1

    return {'imported': imported, 'failed': failed}
