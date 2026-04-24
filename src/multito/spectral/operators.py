"""
Spectral operators for multi-topology conductor optimization.

This module provides Fourier transforms and simple filtering operations to
analyze design variables in the frequency domain. The functions herein
are generic and can be applied to any numeric signal.

Functions:
- forward_fft(signal: Sequence[float]) -> np.ndarray: Compute 1D FFT.
- inverse_fft(spectrum: Sequence[complex]) -> np.ndarray: Compute inverse FFT.
- low_pass_filter(spectrum, cutoff: int) -> np.ndarray: Apply low-pass.
- high_pass_filter(spectrum, cutoff: int) -> np.ndarray: Apply high-pass.
"""

from typing import Sequence
import numpy as np


def forward_fft(signal: Sequence[float]) -> np.ndarray:
    """Compute the discrete Fourier transform of a real-valued signal.

    Args:
        signal: Sequence of real numbers representing the signal.

    Returns:
        Complex-valued numpy array containing the Fourier coefficients.
    """
    return np.fft.fft(signal)


def inverse_fft(spectrum: Sequence[complex]) -> np.ndarray:
    """Compute the inverse discrete Fourier transform.

    Args:
        spectrum: Sequence of complex Fourier coefficients.

    Returns:
        Real-valued numpy array of reconstructed signal.
    """
    return np.fft.ifft(spectrum).real


def low_pass_filter(spectrum: Sequence[complex], cutoff: int) -> np.ndarray:
    """Apply a low-pass filter by zeroing out high-frequency components.

    Args:
        spectrum: Fourier spectrum.
        cutoff: Index of frequency above which to zero.

    Returns:
        Filtered spectrum with high frequency components zeroed.
    """
    filtered = np.array(spectrum, dtype=complex).copy()
    n = len(filtered)
    # Zero out frequencies beyond the cutoff on both sides of the symmetric spectrum
    filtered[cutoff:n - cutoff] = 0
    return filtered


def high_pass_filter(spectrum: Sequence[complex], cutoff: int) -> np.ndarray:
    """Apply a high-pass filter by zeroing out low-frequency components.

    Args:
        spectrum: Fourier spectrum.
        cutoff: Index of frequency below which to zero.

    Returns:
        Filtered spectrum with low frequency components zeroed.
    """
    filtered = np.array(spectrum, dtype=complex).copy()
    # Zero out low frequencies and symmetric high-frequency counterparts
    filtered[:cutoff] = 0
    filtered[-cutoff:] = 0
    return filtered
