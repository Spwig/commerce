import mimetypes

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Configurator3DConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'configurator_3d'
    verbose_name = _('3D Configurator')

    def ready(self):
        # Register 3D file MIME types so mimetypes.guess_type works for uploads
        mimetypes.add_type('model/gltf-binary', '.glb')
        mimetypes.add_type('model/gltf+json', '.gltf')
        mimetypes.add_type('image/hdr', '.hdr')
