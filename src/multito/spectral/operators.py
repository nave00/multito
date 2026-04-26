""""""
Spectral operator and transform tools for frequency-domain analysis.

This module provides basic operations to analyze design variables in
the frequency domain. Functions herein include:

- forward_fft(signal: Sequence[float]) -> np.ndarray: Perform 1D FFT.
- inverse_fft(spectrum: Sequence[complex]) -> np.ndarray: Compute inverse FFT.
- low_pass_filter(spectrum: Sequence[complex], cutoff: float) -> np.ndarray: Apply low-pass.
- high_pass_filter(spectrum: Sequence[complex], cutoff: float) -> np.ndarray: Apply high-pass.
- spectral_operator(k: Sequence[float], epsilon: float, w0: float, k0: float) -> np.ndarray:
  Compute the spectral operator \hat{L}(k) = -epsilon + w0 * (k0**2 - k**2)**2.

These functions help analyze the spectral content of a signal and perform simple
filters and operator evaluations on a real-valued signal.

"""
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
    return
    
    def spectral_operator(k: Sequence[float], epsilon: float, w0: float, k0: float) -> np.ndarray:
    """Compute the spectral operator \hat{L}(k) = -epsilon + w0 * (k0**2 - k**2)**2.

    This operator is used in frequency-domain analyses to model spectral properties.

    Args:
        k: Sequence of wavenumbers at which to evaluate the operator.
        epsilon: The parameter \u03B5 controlling the baseline value.
        w0: Weight parameter w\u2080 scaling the quartic term.
        k0: Reference wavenumber k\u2080.

    Returns:
        Numpy array of operator values evaluated at each wavenumber in `k`.
    """
    k_array = np.array(k, dtype=float)
    return -epsilon + w0 * (k0**2 - k_array**2)**2

