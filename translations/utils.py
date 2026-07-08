"""
Utility functions for the translation service
"""
import os
import psutil
import hashlib
import requests
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from django.utils.translation import gettext as _
from django.conf import settings

logger = logging.getLogger(__name__)


class SystemValidator:
    """Validate system requirements for translation service"""

    MIN_CPU_CORES = 4
    MIN_RAM_GB = 8
    MIN_DISK_GB = 3
    RECOMMENDED_CPU_CORES = 8
    RECOMMENDED_RAM_GB = 16
    RECOMMENDED_DISK_GB = 10

    def check_requirements(self) -> Dict:
        """
        Check if system meets minimum requirements
        Returns dict with validation results
        """
        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        ram_gb = memory.total / (1024**3)
        disk_free_gb = disk.free / (1024**3)

        result = {
            'meets_requirements': True,
            'meets_recommended': True,
            'cpu_cores': cpu_count,
            'ram_gb': ram_gb,
            'disk_free_gb': disk_free_gb,
            'warnings': [],
            'recommendations': [],
            'status': 'success'
        }

        # Check minimum requirements
        if cpu_count < self.MIN_CPU_CORES:
            result['meets_requirements'] = False
            result['warnings'].append(
                _('CPU: %(cores)d cores (minimum: %(min)d)') % {
                    'cores': cpu_count,
                    'min': self.MIN_CPU_CORES
                }
            )

        if ram_gb < self.MIN_RAM_GB:
            result['meets_requirements'] = False
            result['warnings'].append(
                _('RAM: %(ram).1f GB (minimum: %(min)d GB)') % {
                    'ram': ram_gb,
                    'min': self.MIN_RAM_GB
                }
            )

        if disk_free_gb < self.MIN_DISK_GB:
            result['meets_requirements'] = False
            result['warnings'].append(
                _('Disk: %(disk).1f GB free (minimum: %(min)d GB)') % {
                    'disk': disk_free_gb,
                    'min': self.MIN_DISK_GB
                }
            )

        # Check recommended specifications
        if cpu_count < self.RECOMMENDED_CPU_CORES:
            result['meets_recommended'] = False
            result['recommendations'].append(
                _('CPU: Consider upgrading to %(rec)d cores for better performance') % {
                    'rec': self.RECOMMENDED_CPU_CORES
                }
            )

        if ram_gb < self.RECOMMENDED_RAM_GB:
            result['meets_recommended'] = False
            result['recommendations'].append(
                _('RAM: %(rec)d GB recommended for large batch translations') % {
                    'rec': self.RECOMMENDED_RAM_GB
                }
            )

        if disk_free_gb < self.RECOMMENDED_DISK_GB:
            result['meets_recommended'] = False
            result['recommendations'].append(
                _('Disk: %(rec)d GB free space recommended for multiple models') % {
                    'rec': self.RECOMMENDED_DISK_GB
                }
            )

        # Set overall status
        if not result['meets_requirements']:
            result['status'] = 'error'
            result['message'] = _(
                'Your system doesn\'t meet the requirements. '
                'Minimum: %(min_cpu)d vCPU/%(min_ram)dGB RAM/%(min_disk)dGB free disk. '
                'You may enable AI translation, but performance may be slow '
                'and could impact shoppers during bulk translations. '
                'Consider scheduling jobs off-peak or use an external provider.'
            ) % {
                'min_cpu': self.MIN_CPU_CORES,
                'min_ram': self.MIN_RAM_GB,
                'min_disk': self.MIN_DISK_GB
            }
        elif not result['meets_recommended']:
            result['status'] = 'warning'
            result['message'] = _(
                'Your system meets minimum requirements but not recommended specs. '
                'Performance may be limited for large-scale translations.'
            )
        else:
            result['status'] = 'success'
            result['message'] = _(
                'Congratulations! Your server supports the minimum requirements '
                'to run our AI translation module!'
            )

        # Check Docker availability
        result['docker_available'] = self._check_docker()

        # Check translator service
        result['translator_service'] = self._check_translator_service()

        return result

    def _check_docker(self) -> bool:
        """Check if Docker is available"""
        try:
            import subprocess
            result = subprocess.run(
                ['docker', 'ps'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False

    def _check_translator_service(self) -> Dict:
        """Check translator service status"""
        from .client import get_translator_client
        client = get_translator_client()

        if client.is_available():
            info = client.get_system_info()
            return {
                'available': True,
                'status': 'running',
                'info': info
            }
        else:
            return {
                'available': False,
                'status': 'offline',
                'info': None
            }

    def get_gpu_info(self) -> Optional[Dict]:
        """Get GPU information if available"""
        try:
            import subprocess
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                gpus = []
                for line in lines:
                    parts = line.split(', ')
                    if len(parts) >= 2:
                        gpus.append({
                            'name': parts[0],
                            'memory': parts[1]
                        })
                return {
                    'available': True,
                    'count': len(gpus),
                    'devices': gpus
                }
        except:
            pass
        return {'available': False}


class ModelManager:
    """Manage translation models"""

    def __init__(self):
        self.models_dir = Path('/models')
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def get_available_models(self) -> List[Dict]:
        """Get list of available models to download"""
        return [
            {
                'name': 'm2m100-418m',
                'display_name': 'M2M100 418M (Base)',
                'size_mb': 1800,
                'languages': ['en', 'es', 'fr', 'de', 'pt', 'zh', 'ja'],
                'description': _('General purpose multilingual model')
            },
            {
                'name': 'm2m100-1.2b',
                'display_name': 'M2M100 1.2B (Large)',
                'size_mb': 4800,
                'languages': ['en', 'es', 'fr', 'de', 'pt', 'zh', 'ja', 'ar', 'ru'],
                'description': _('Higher quality translations, requires more resources')
            },
            {
                'name': 'nllb-200-600m',
                'display_name': 'NLLB 200 600M',
                'size_mb': 2400,
                'languages': ['en', 'es', 'fr', 'de', 'pt', 'zh', 'ja'] + ['ar', 'hi', 'tr'],
                'description': _('Supports 200+ languages')
            }
        ]

    def get_installed_models(self) -> List[Dict]:
        """Get list of installed models"""
        installed = []
        for model_dir in self.models_dir.iterdir():
            if model_dir.is_dir():
                size = self._get_directory_size(model_dir)
                installed.append({
                    'name': model_dir.name,
                    'path': str(model_dir),
                    'size_mb': size / (1024 * 1024)
                })
        return installed

    def _get_directory_size(self, path: Path) -> int:
        """Get total size of directory in bytes"""
        total = 0
        for entry in path.rglob('*'):
            if entry.is_file():
                total += entry.stat().st_size
        return total

    def download_model(self, model_name: str, callback=None) -> bool:
        """
        Download a model (placeholder - actual implementation would download from HuggingFace)
        callback: function(progress_percent, status_message)
        """
        model_path = self.models_dir / model_name

        # This would actually download the model
        # For now, just create the directory
        model_path.mkdir(parents=True, exist_ok=True)

        if callback:
            callback(100, _('Model downloaded successfully'))

        return True

    def delete_model(self, model_name: str) -> bool:
        """Delete an installed model"""
        model_path = self.models_dir / model_name
        if model_path.exists():
            import shutil
            shutil.rmtree(model_path)
            return True
        return False

    def estimate_download_time(self, size_mb: float) -> float:
        """Estimate download time in seconds based on connection speed"""
        # Assume 10 Mbps connection
        speed_mbps = 10
        speed_mb_per_sec = speed_mbps / 8
        return size_mb / speed_mb_per_sec


class TranslationHelper:
    """Helper functions for translation operations"""

    @staticmethod
    def calculate_checksum(text: str) -> str:
        """Calculate MD5 checksum of text"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    @staticmethod
    def estimate_translation_time(text_length: int, model_type: str = 'base') -> float:
        """Estimate translation time in seconds"""
        # Rough estimates based on model type
        if model_type == 'base':
            chars_per_second = 100
        elif model_type == 'large':
            chars_per_second = 50
        else:
            chars_per_second = 75

        return text_length / chars_per_second

    @staticmethod
    def batch_texts(texts: List[str], max_batch_size: int = 100) -> List[List[str]]:
        """Split texts into batches for processing"""
        batches = []
        current_batch = []
        current_size = 0

        for text in texts:
            if len(current_batch) >= max_batch_size:
                batches.append(current_batch)
                current_batch = []
                current_size = 0

            current_batch.append(text)
            current_size += len(text)

            # Also limit by total character count
            if current_size > 10000:
                batches.append(current_batch)
                current_batch = []
                current_size = 0

        if current_batch:
            batches.append(current_batch)

        return batches

    @staticmethod
    def get_language_name(code: str) -> str:
        """Get display name for language code"""
        language_names = {
            'en': _('English'),
            'es': _('Spanish'),
            'fr': _('French'),
            'de': _('German'),
            'pt': _('Portuguese'),
            'zh': _('Chinese'),
            'zh-hans': _('Simplified Chinese'),
            'ja': _('Japanese'),
            'ar': _('Arabic'),
            'ru': _('Russian'),
            'hi': _('Hindi'),
            'tr': _('Turkish'),
        }
        return language_names.get(code, code.upper())


class ProviderValidator:
    """Validate external translation providers"""

    @staticmethod
    def test_deepl(api_key: str, endpoint: str = None) -> Tuple[bool, str]:
        """Test DeepL API connection"""
        try:
            url = endpoint or 'https://api.deepl.com/v2/languages'
            response = requests.get(
                url,
                headers={'Authorization': f'DeepL-Auth-Key {api_key}'},
                timeout=5
            )
            if response.status_code == 200:
                return True, _('DeepL connection successful')
            else:
                return False, _('Invalid API key or endpoint')
        except Exception as e:
            return False, str(e)

    @staticmethod
    def test_google(api_key: str) -> Tuple[bool, str]:
        """Test Google Translate API connection"""
        try:
            url = 'https://translation.googleapis.com/language/translate/v2/languages'
            response = requests.get(
                url,
                params={'key': api_key},
                timeout=5
            )
            if response.status_code == 200:
                return True, _('Google Translate connection successful')
            else:
                return False, _('Invalid API key')
        except Exception as e:
            return False, str(e)

    @staticmethod
    def test_azure(api_key: str, endpoint: str, region: str) -> Tuple[bool, str]:
        """Test Azure Translator API connection"""
        try:
            url = f'{endpoint}/languages'
            response = requests.get(
                url,
                headers={
                    'Ocp-Apim-Subscription-Key': api_key,
                    'Ocp-Apim-Subscription-Region': region
                },
                params={'api-version': '3.0'},
                timeout=5
            )
            if response.status_code == 200:
                return True, _('Azure Translator connection successful')
            else:
                return False, _('Invalid API key or configuration')
        except Exception as e:
            return False, str(e)