# tts_normalizer/__init__.py

import logging
import json

# Importa todas las funciones, incluida la última
from .normalizacion.normalize_abbreviations import normalize_abbreviations
from .normalizacion.normalize_acronyms import normalize_acronyms
from .normalizacion.normalize_identifiers import normalize_identifiers # <-- NUEVA
from .normalizacion.normalize_times import normalize_times
from .normalizacion.normalize_ordinals import normalize_ordinals
from .normalizacion.normalize_roman_numerals import normalize_roman_numerals
from .normalizacion.normalize_ranges_fractions import normalize_ranges_fractions
from .normalizacion.normalize_units_symbols import normalize_units_symbols
from .normalizacion.normalize_numbers import normalize_numbers

# La función pública principal ahora tiene el pipeline completo y final
def normalize_text(raw_text: str, logger=None) -> str:
    """
    Aplica el pipeline completo de normalización de texto para TTS.
    """
    processed_text = normalize_abbreviations(raw_text, logger)
    processed_text = normalize_acronyms(processed_text, logger)
    processed_text = normalize_identifiers(processed_text, logger)
    processed_text = normalize_times(processed_text, logger)
    processed_text = normalize_ordinals(processed_text, logger)
    processed_text = normalize_roman_numerals(processed_text, logger)
    processed_text = normalize_ranges_fractions(processed_text, logger)
    processed_text = normalize_units_symbols(processed_text, logger)
    processed_text = normalize_numbers(processed_text, logger)
    return processed_text

# La función setup_default_logger no cambia
def setup_default_logger():
    for handler in logging.root.handlers[:]: logging.root.removeHandler(handler)
    handler = logging.FileHandler('normalization.log', mode='w', encoding='utf-8')
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger('tts_normalizer_package')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger