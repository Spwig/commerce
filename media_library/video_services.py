import os
import io
import subprocess
import json
import logging
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image

logger = logging.getLogger(__name__)


class VideoProcessor:
    """Service for processing videos - conversion, optimization, and thumbnail generation"""

    def __init__(self):
        self.video_settings = getattr(settings, 'MEDIA_LIBRARY_SETTINGS', {}).get('VIDEO_FORMATS', {})
        self.thumbnail_time = getattr(settings, 'MEDIA_LIBRARY_SETTINGS', {}).get('VIDEO_THUMBNAIL_TIME', '00:00:02')
        self.video_resolutions = getattr(settings, 'MEDIA_LIBRARY_SETTINGS', {}).get('VIDEO_RESOLUTIONS', {})

    def probe_video(self, video_path):
        """
        Extract video metadata using ffprobe

        Returns:
            Dictionary with video metadata
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                video_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)

            # Extract relevant metadata
            metadata = {
                'duration': None,
                'width': None,
                'height': None,
                'frame_rate': None,
                'bitrate': None,
                'video_codec': None,
                'audio_codec': None,
                'format': data.get('format', {}).get('format_name'),
                'size': data.get('format', {}).get('size'),
            }

            # Get format-level metadata
            if 'format' in data:
                metadata['duration'] = float(data['format'].get('duration', 0))
                metadata['bitrate'] = int(data['format'].get('bit_rate', 0))

            # Get stream-level metadata
            for stream in data.get('streams', []):
                if stream['codec_type'] == 'video' and metadata['width'] is None:
                    metadata['width'] = stream.get('width')
                    metadata['height'] = stream.get('height')
                    metadata['video_codec'] = stream.get('codec_name')

                    # Calculate frame rate
                    if 'r_frame_rate' in stream:
                        num, den = stream['r_frame_rate'].split('/')
                        if den != '0':
                            metadata['frame_rate'] = float(num) / float(den)

                elif stream['codec_type'] == 'audio' and metadata['audio_codec'] is None:
                    metadata['audio_codec'] = stream.get('codec_name')

            return metadata

        except subprocess.CalledProcessError as e:
            logger.error(f"Error probing video: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error probing video: {e}")
            return None

    def extract_thumbnail(self, video_path, timestamp=None):
        """
        Extract a thumbnail image from video at specified timestamp

        Args:
            video_path: Path to video file
            timestamp: Time to extract frame (format: HH:MM:SS or seconds)

        Returns:
            ContentFile with thumbnail image
        """
        try:
            timestamp = timestamp or self.thumbnail_time

            # Create temp output path
            temp_output = f"/tmp/thumbnail_{os.getpid()}.jpg"

            cmd = [
                'ffmpeg',
                '-ss', str(timestamp),
                '-i', video_path,
                '-vframes', '1',
                '-vf', 'scale=800:-1',  # Max width 800px, maintain aspect ratio
                '-q:v', '2',  # High quality JPEG
                temp_output,
                '-y'  # Overwrite output
            ]

            subprocess.run(cmd, capture_output=True, check=True)

            # Read the generated thumbnail
            with open(temp_output, 'rb') as f:
                content = ContentFile(f.read())

            # Clean up temp file
            os.remove(temp_output)

            return content

        except subprocess.CalledProcessError as e:
            logger.error(f"Error extracting thumbnail: {e.stderr}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error extracting thumbnail: {e}")
            return None

    def convert_to_webm_av1(self, video_path, output_path=None, crf=30, preset=6, progress_callback=None):
        """
        Convert video to WebM with AV1 codec

        Args:
            video_path: Input video path
            output_path: Output path (optional, generates temp file if not provided)
            crf: Constant Rate Factor (lower = better quality, 0-63)
            preset: Encoding speed preset (0-13, higher = faster)
            progress_callback: Optional callback function for progress updates

        Returns:
            Path to converted video or None on error
        """
        try:
            if not output_path:
                output_path = f"/tmp/video_{os.getpid()}.webm"

            # Get video duration for progress tracking
            duration = None
            if progress_callback:
                metadata = self.probe_video(video_path)
                duration = metadata.get('duration') if metadata else None

            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-c:v', 'libsvtav1',  # Use SVT-AV1 encoder (faster than libaom)
                '-crf', str(crf),
                '-preset', str(preset),
                '-c:a', 'libopus',  # Opus audio codec
                '-b:a', '128k',
                '-f', 'webm',
                '-progress', 'pipe:1',  # Output progress to stdout
                '-stats_period', '1',   # Update every second
                output_path,
                '-y'
            ]

            logger.info(f"Converting video to WebM/AV1: {' '.join(cmd)}")

            if progress_callback and duration:
                # Run with progress monitoring
                import re
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                for line in process.stdout:
                    # Parse progress from ffmpeg output
                    if 'out_time_ms=' in line:
                        match = re.search(r'out_time_ms=(\d+)', line)
                        if match:
                            time_ms = int(match.group(1))
                            time_seconds = time_ms / 1000000  # Convert microseconds to seconds
                            progress = min(int((time_seconds / duration) * 100), 100)
                            progress_callback(progress)

                process.wait()
                if process.returncode != 0:
                    stderr = process.stderr.read()
                    raise subprocess.CalledProcessError(process.returncode, cmd, stderr=stderr)
            else:
                # Run without progress monitoring
                subprocess.run(cmd, capture_output=True, check=True)

            return output_path

        except subprocess.CalledProcessError as e:
            logger.error(f"Error converting to WebM/AV1: {e.stderr}")
            # Fallback to VP9 if AV1 encoder not available
            return self.convert_to_webm_vp9(video_path, output_path)
        except Exception as e:
            logger.error(f"Unexpected error converting to WebM/AV1: {e}")
            return None

    def convert_to_webm_vp9(self, video_path, output_path=None, crf=30, progress_callback=None):
        """
        Convert video to WebM with VP9 codec (fallback if AV1 not available)

        Args:
            video_path: Input video path
            output_path: Output path
            crf: Constant Rate Factor
            progress_callback: Optional callback function(progress_percent) for progress updates

        Returns:
            Path to converted video or None on error
        """
        try:
            if not output_path:
                output_path = f"/tmp/video_{os.getpid()}.webm"

            # Get video duration for progress calculation
            duration = None
            if progress_callback:
                metadata = self.probe_video(video_path)
                if metadata:
                    duration = metadata.get('duration')

            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-c:v', 'libvpx-vp9',
                '-crf', str(crf),
                '-b:v', '0',  # Use CRF mode
                '-c:a', 'libopus',
                '-b:a', '128k',
                '-f', 'webm',
            ]

            # Add progress output if callback provided
            if progress_callback and duration:
                cmd.extend(['-progress', 'pipe:1'])

            cmd.extend([output_path, '-y'])

            logger.info(f"Converting video to WebM/VP9: {' '.join(cmd)}")

            if progress_callback and duration:
                # Run with progress monitoring
                import re
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                for line in process.stdout:
                    # Parse progress from ffmpeg output
                    if 'out_time_ms=' in line:
                        match = re.search(r'out_time_ms=(\d+)', line)
                        if match:
                            time_ms = int(match.group(1))
                            time_seconds = time_ms / 1000000  # Convert microseconds to seconds
                            progress = min(int((time_seconds / duration) * 100), 100)
                            progress_callback(progress)

                process.wait()
                if process.returncode != 0:
                    stderr = process.stderr.read()
                    raise subprocess.CalledProcessError(process.returncode, cmd, stderr=stderr)
            else:
                # Run without progress monitoring
                subprocess.run(cmd, capture_output=True, check=True)

            return output_path

        except subprocess.CalledProcessError as e:
            logger.error(f"Error converting to WebM/VP9: {e.stderr}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error converting to WebM/VP9: {e}")
            return None

    def convert_to_mp4_h265(self, video_path, output_path=None, crf=28, progress_callback=None):
        """
        Convert video to MP4 with H.265/HEVC codec for better compression

        Args:
            video_path: Input video path
            output_path: Output path
            crf: Constant Rate Factor (28 is roughly equivalent to H.264 crf 23)
            progress_callback: Optional callback function(progress_percent) for progress updates

        Returns:
            Path to converted video or None on error
        """
        try:
            if not output_path:
                output_path = f"/tmp/video_{os.getpid()}_h265.mp4"

            # Get video duration for progress calculation
            duration = None
            if progress_callback:
                metadata = self.probe_video(video_path)
                if metadata:
                    duration = metadata.get('duration')

            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-c:v', 'libx265',
                '-preset', 'medium',
                '-crf', str(crf),
                '-c:a', 'aac',
                '-b:a', '128k',
                '-tag:v', 'hvc1',  # Better compatibility for Apple devices
                '-movflags', '+faststart',
                '-pix_fmt', 'yuv420p',
            ]

            # Add progress output if callback provided
            if progress_callback and duration:
                cmd.extend(['-progress', 'pipe:1'])

            cmd.extend([output_path, '-y'])

            logger.info(f"Converting video to MP4/H.265: {' '.join(cmd)}")

            if progress_callback and duration:
                # Run with progress monitoring
                import re
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                for line in process.stdout:
                    # Parse progress from ffmpeg output
                    if 'out_time_ms=' in line:
                        match = re.search(r'out_time_ms=(\d+)', line)
                        if match:
                            time_ms = int(match.group(1))
                            time_seconds = time_ms / 1000000  # Convert microseconds to seconds
                            progress = min(int((time_seconds / duration) * 100), 100)
                            progress_callback(progress)

                process.wait()
                if process.returncode != 0:
                    stderr = process.stderr.read()
                    raise subprocess.CalledProcessError(process.returncode, cmd, stderr=stderr)
            else:
                # Run without progress monitoring
                subprocess.run(cmd, capture_output=True, check=True)

            return output_path

        except subprocess.CalledProcessError as e:
            logger.error(f"Error converting to MP4/H.265: {e.stderr}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error converting to MP4/H.265: {e}")
            return None

    def convert_to_mp4_h264(self, video_path, output_path=None, crf=23):
        """
        Convert video to MP4 with H.264 codec for maximum compatibility

        Args:
            video_path: Input video path
            output_path: Output path
            crf: Constant Rate Factor (lower = better quality, 0-51)

        Returns:
            Path to converted video or None on error
        """
        try:
            if not output_path:
                output_path = f"/tmp/video_{os.getpid()}.mp4"

            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', str(crf),
                '-c:a', 'aac',
                '-b:a', '128k',
                '-movflags', '+faststart',  # Enable fast start for web streaming
                '-pix_fmt', 'yuv420p',  # Ensure compatibility
                output_path,
                '-y'
            ]

            logger.info(f"Converting video to MP4/H.264: {' '.join(cmd)}")
            subprocess.run(cmd, capture_output=True, check=True)

            return output_path

        except subprocess.CalledProcessError as e:
            logger.error(f"Error converting to MP4/H.264: {e.stderr}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error converting to MP4/H.264: {e}")
            return None

    def generate_adaptive_versions(self, video_path, resolutions=None):
        """
        Generate multiple resolution versions for adaptive streaming

        Args:
            video_path: Input video path
            resolutions: Dict of resolution names and sizes (e.g., {'720p': '1280x720'})

        Returns:
            Dict of resolution names to file paths
        """
        resolutions = resolutions or self.video_resolutions or {
            '1080p': '1920x1080',
            '720p': '1280x720',
            '480p': '854x480',
        }

        versions = {}

        for name, resolution in resolutions.items():
            try:
                output_path = f"/tmp/video_{os.getpid()}_{name}.mp4"

                cmd = [
                    'ffmpeg',
                    '-i', video_path,
                    '-c:v', 'libx264',
                    '-preset', 'medium',
                    '-crf', '23',
                    '-vf', f'scale={resolution}:force_original_aspect_ratio=decrease,pad={resolution}:(ow-iw)/2:(oh-ih)/2',
                    '-c:a', 'aac',
                    '-b:a', '128k',
                    '-movflags', '+faststart',
                    output_path,
                    '-y'
                ]

                subprocess.run(cmd, capture_output=True, check=True)
                versions[name] = output_path

            except subprocess.CalledProcessError as e:
                logger.error(f"Error generating {name} version: {e.stderr}")
            except Exception as e:
                logger.error(f"Unexpected error generating {name} version: {e}")

        return versions

    def optimize_for_web(self, video_path, max_size_mb=50):
        """
        Optimize video for web delivery with size constraints

        Args:
            video_path: Input video path
            max_size_mb: Maximum output size in megabytes

        Returns:
            Path to optimized video
        """
        try:
            # Get video duration to calculate target bitrate
            metadata = self.probe_video(video_path)
            if not metadata or not metadata['duration']:
                return None

            duration_seconds = metadata['duration']

            # Calculate target bitrate to achieve desired file size
            # Formula: bitrate = (file_size_bits) / duration_seconds
            target_size_bits = max_size_mb * 8 * 1024 * 1024
            target_bitrate = int(target_size_bits / duration_seconds)

            # Reserve 128kbps for audio
            video_bitrate = target_bitrate - 128000

            output_path = f"/tmp/video_{os.getpid()}_optimized.mp4"

            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-c:v', 'libx264',
                '-b:v', str(video_bitrate),
                '-maxrate', str(int(video_bitrate * 1.5)),
                '-bufsize', str(video_bitrate * 2),
                '-preset', 'medium',
                '-c:a', 'aac',
                '-b:a', '128k',
                '-movflags', '+faststart',
                output_path,
                '-y'
            ]

            subprocess.run(cmd, capture_output=True, check=True)

            return output_path

        except Exception as e:
            logger.error(f"Error optimizing video for web: {e}")
            return None

    def check_ffmpeg_available(self):
        """Check if ffmpeg is installed and available"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except:
            return False

    def get_supported_encoders(self):
        """Get list of available video encoders"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-encoders'],
                capture_output=True,
                text=True,
                check=True
            )

            encoders = []
            for line in result.stdout.split('\n'):
                if 'libsvtav1' in line:
                    encoders.append('av1')
                elif 'libvpx-vp9' in line:
                    encoders.append('vp9')
                elif 'libx264' in line:
                    encoders.append('h264')

            return encoders

        except:
            return []