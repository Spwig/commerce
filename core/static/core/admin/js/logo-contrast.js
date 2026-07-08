/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Logo Contrast Enhancement
 *
 * Automatically detects logo luminance and applies appropriate backplate
 * to ensure visibility across light/dark themes.
 *
 * Usage: Add `data-auto-contrast` attribute to logo containers:
 *   <div class="logo-plate" data-auto-contrast>
 *     <img src="/path/to/logo.png" alt="Brand">
 *   </div>
 *
 * The script will automatically apply:
 *   .logo-plate--light (for dark logos)
 *   .logo-plate--dark (for light logos)
 *   .logo-plate--halo (if contrast still < 3:1)
 */

(function() {
    'use strict';

    const MIN_CONTRAST_RATIO = 3.0; // Aim for >= 3:1 for visual comfort
    const CACHE_VERSION = 'v2'; // Increment when algorithm changes
    const CACHE_PREFIX = 'logo-lum:' + CACHE_VERSION + ':';
    const SAMPLE_SIZE = 160; // Max width for analysis (performance optimization)

    /**
     * Calculate relative luminance (WCAG 2.0 formula)
     * @param {number} r - Red (0-255)
     * @param {number} g - Green (0-255)
     * @param {number} b - Blue (0-255)
     * @returns {number} Relative luminance (0-1)
     */
    function calculateLuminance(r, g, b) {
        // Convert to sRGB
        const srgb = [r, g, b].map(v => v / 255);

        // Convert to linear RGB
        const linear = srgb.map(v => {
            return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
        });

        // Calculate relative luminance (WCAG formula)
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2];
    }

    /**
     * Calculate contrast ratio between two luminance values
     * @param {number} L1 - First luminance
     * @param {number} L2 - Second luminance
     * @returns {number} Contrast ratio (1-21)
     */
    function contrastRatio(L1, L2) {
        const lighter = Math.max(L1, L2);
        const darker = Math.min(L1, L2);
        return (lighter + 0.05) / (darker + 0.05);
    }

    /**
     * Get current theme background luminance for blending calculations
     * @returns {number} Background luminance (0-1)
     */
    function getThemeBackgroundLuminance() {
        const isDark = document.documentElement.dataset.theme === 'dark';
        // Dark theme: ~#1a1d26 (very dark blue-gray) ≈ 0.05
        // Light theme: ~#f8f9fa (very light gray) ≈ 0.95
        return isDark ? 0.05 : 0.95;
    }

    /**
     * Analyze image and calculate effective luminance (accounting for transparency)
     * @param {HTMLImageElement} img - Image element to analyze
     * @returns {Promise<number>} Effective median luminance (0-1)
     */
    async function analyzeImageLuminance(img) {
        // Check cache first (cache key includes theme for transparency blending)
        const isDark = document.documentElement.dataset.theme === 'dark';
        const cacheKey = CACHE_PREFIX + img.src + ':' + (isDark ? 'dark' : 'light');
        const cached = localStorage.getItem(cacheKey);
        if (cached) {
            return parseFloat(cached);
        }

        return new Promise((resolve) => {
            // Create canvas for pixel analysis
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d', { willReadFrequently: true });

            // Sample at smaller size for performance
            const naturalWidth = img.naturalWidth || SAMPLE_SIZE;
            const naturalHeight = img.naturalHeight || SAMPLE_SIZE;
            const width = Math.min(SAMPLE_SIZE, naturalWidth);
            const height = Math.floor((width / naturalWidth) * naturalHeight) || width;

            canvas.width = Math.max(1, width);
            canvas.height = Math.max(1, height);

            try {
                // Draw image to canvas
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

                // Get pixel data
                const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const data = imageData.data;

                // Get theme background luminance for alpha blending
                const bgLuminance = getThemeBackgroundLuminance();

                // Calculate effective luminance for each pixel (blend with background based on alpha)
                const luminanceValues = [];
                let totalPixels = 0;
                let opaquePixels = 0;

                for (let i = 0; i < data.length; i += 4) {
                    totalPixels++;
                    const alpha = data[i + 3] / 255; // Normalize alpha to 0-1

                    // Skip fully transparent pixels (alpha < 0.04)
                    if (alpha < 0.04) continue;

                    opaquePixels++;
                    const r = data[i];
                    const g = data[i + 1];
                    const b = data[i + 2];
                    const pixelLum = calculateLuminance(r, g, b);

                    // Calculate effective luminance by blending with background
                    // Formula: effectiveLum = (alpha × pixelLum) + ((1 - alpha) × bgLum)
                    const effectiveLum = (alpha * pixelLum) + ((1 - alpha) * bgLuminance);
                    luminanceValues.push(effectiveLum);
                }

                // Calculate median luminance
                let medianLum = 0.5; // Default fallback

                if (luminanceValues.length > 0) {
                    luminanceValues.sort((a, b) => a - b);
                    const middleIndex = Math.floor(luminanceValues.length / 2);
                    medianLum = luminanceValues[middleIndex];
                } else {
                    // Fully transparent image - use background luminance
                    medianLum = bgLuminance;
                }

                // Cache result (theme-specific due to alpha blending)
                localStorage.setItem(cacheKey, String(medianLum));

                resolve(medianLum);
            } catch (error) {
                // If analysis fails (CORS, etc.), make an educated guess based on theme
                // In dark theme, assume most logos need light backplate (safer default)
                // In light theme, assume most logos need dark backplate
                const isDark = document.documentElement.dataset.theme === 'dark';
                const fallbackLum = isDark ? 0.2 : 0.7; // Dark logos on dark theme, light logos on light theme
                console.warn('Logo luminance analysis failed (likely CORS):', error.message);
                console.info('Using fallback luminance:', fallbackLum);
                resolve(fallbackLum);
            }
        });
    }

    /**
     * Get theme-specific backplate luminance values
     * @returns {Object} Plate luminance values
     */
    function getThemePlateLuminance() {
        const isDark = document.documentElement.dataset.theme === 'dark';

        return {
            // Light plate (for dark logos)
            plateLight: isDark ? 0.15 : 0.95,
            // Dark plate (for light logos)
            plateDark: isDark ? 0.85 : 0.12
        };
    }

    /**
     * Ensure logo has sufficient contrast with backplate
     * @param {HTMLElement} container - Logo container with data-auto-contrast
     */
    async function ensureLogoContrast(container) {
        // Find img or svg within container
        const img = container.querySelector('img, svg');

        if (!img) {
            // No image found, apply default
            container.classList.add('logo-plate--light');
            return;
        }

        // For SVG elements, prefer currentColor method (light plate default)
        if (img.tagName === 'SVG') {
            container.classList.add('logo-plate--light');
            return;
        }

        // Wait for image to load if needed
        if (!img.complete || img.naturalWidth === 0) {
            img.addEventListener('load', () => ensureLogoContrast(container), { once: true });
            return;
        }

        try {
            // Analyze logo luminance
            const logoLum = await analyzeImageLuminance(img);

            // Get theme backplate luminance values
            const { plateLight, plateDark } = getThemePlateLuminance();

            // Calculate contrast ratios for both plates
            const contrastLight = contrastRatio(logoLum, plateLight);
            const contrastDark = contrastRatio(logoLum, plateDark);

            // Choose plate with better contrast
            const useLightPlate = contrastLight >= contrastDark;
            const bestContrast = Math.max(contrastLight, contrastDark);

            // Apply appropriate class
            container.classList.add(useLightPlate ? 'logo-plate--light' : 'logo-plate--dark');

            // If even the best choice has low contrast, add halo
            if (bestContrast < MIN_CONTRAST_RATIO) {
                container.classList.add('logo-plate--halo');
            }

        } catch (error) {
            // Fallback on error
            console.warn('Logo contrast detection failed:', error);
            container.classList.add('logo-plate--light');
        }
    }

    /**
     * Initialize contrast detection for all marked containers
     */
    function initLogoContrast() {
        const containers = document.querySelectorAll('[data-auto-contrast]');
        containers.forEach(container => {
            // Skip if already processed
            if (container.classList.contains('logo-plate--light') ||
                container.classList.contains('logo-plate--dark')) {
                return;
            }

            ensureLogoContrast(container);
        });
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initLogoContrast);
    } else {
        initLogoContrast();
    }

    // Re-initialize on theme change (if theme switcher exists)
    document.addEventListener('themeChanged', () => {
        // Clear existing plate classes
        document.querySelectorAll('[data-auto-contrast]').forEach(container => {
            container.classList.remove('logo-plate--light', 'logo-plate--dark', 'logo-plate--halo');
        });

        // Re-analyze
        initLogoContrast();
    });

    // Export for manual triggering if needed
    window.logoContrast = {
        init: initLogoContrast,
        analyze: ensureLogoContrast
    };

})();
