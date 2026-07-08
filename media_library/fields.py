from django import forms
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import models
from .widgets import MediaLibrarySelectWidget
from .models import MediaAsset
import requests
from urllib.parse import urlparse
import os


class MediaLibraryImageField(forms.ImageField):
    """
    A form field that allows selecting images from the media library
    instead of uploading files directly
    """
    widget = MediaLibrarySelectWidget
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = MediaLibrarySelectWidget()
    
    def to_python(self, data):
        """
        Convert the selected media library URL to a file object
        """
        if not data:
            return None
            
        # If it's already a file, return it
        if hasattr(data, 'read'):
            return super().to_python(data)
        
        # If it's a string (URL from media library)
        if isinstance(data, str):
            # Check if it's a media library URL
            if '/media/' in data:
                # Try to find the MediaAsset
                try:
                    # Extract the filename from the URL
                    filename = os.path.basename(urlparse(data).path)
                    
                    # Find the MediaAsset by filename
                    media_asset = MediaAsset.objects.filter(
                        models.Q(original_file__icontains=filename) |
                        models.Q(webp_file__icontains=filename)
                    ).first()
                    
                    if media_asset:
                        # Return the original file if available, otherwise webp
                        return media_asset.original_file or media_asset.webp_file
                    else:
                        # If not found in media library, try to get the file directly
                        if default_storage.exists(data.replace('/media/', '')):
                            return default_storage.open(data.replace('/media/', ''))
                        
                except Exception as e:
                    print(f"Error processing media library selection: {e}")
                    return None
            
            # If it's an external URL, download it (be careful with this)
            elif data.startswith('http'):
                try:
                    response = requests.get(data)
                    if response.status_code == 200:
                        filename = os.path.basename(urlparse(data).path) or 'downloaded_image'
                        return ContentFile(response.content, name=filename)
                except Exception as e:
                    print(f"Error downloading image: {e}")
                    return None
        
        return super().to_python(data)