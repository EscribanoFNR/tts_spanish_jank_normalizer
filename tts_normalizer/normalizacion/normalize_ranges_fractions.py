import re
import json
from num2words import num2words

def normalize_ranges_fractions(text: str, logger=None) -> str:
    """
    Busca y normaliza rangos numéricos (ej: 20-25) y fracciones (ej: 3/4).
    """
    original_text = text
    modifications = []

    # --- Patrón 1: Rangos numéricos (no cambia) ---
    pattern_range = re.compile(r'\b(\d+)\s*-\s*(\d+)\b')
    def range_replacer(match):
        num1_str, num2_str = match.groups()
        text_num1 = num2words(int(num1_str), lang='es')
        text_num2 = num2words(int(num2_str), lang='es')
        final_text = f"{text_num1} a {text_num2}"
        modifications.append({"detectado": match.group(0), "aplicado": final_text})
        return final_text
    text = pattern_range.sub(range_replacer, text)

    # --- Patrón 2: Fracciones (con corrección) ---
    pattern_fraction = re.compile(r'\b(\d+)/(\d+)\b')
    def fraction_replacer(match):
        numerator_str, denominator_str = match.groups()
        numerator_int = int(numerator_str)

        text_numerator = num2words(numerator_int, lang='es')
        
        # --- LÓGICA CORREGIDA ---
        # Si el numerador es 1, usamos "un" en lugar de "uno" para el masculino.
        if numerator_int == 1:
            text_numerator = "un"
        # --- FIN DE LA CORRECCIÓN ---

        denominator_int = int(denominator_str)
        if denominator_int == 2:
            text_denominator = "medios" if numerator_int > 1 else "medio"
        elif denominator_int == 3:
            text_denominator = "tercios"
        else:
            text_denominator = num2words(denominator_int, to='ordinal', lang='es') + ('s' if numerator_int > 1 else '')

        final_text = f"{text_numerator} {text_denominator}"
        modifications.append({"detectado": match.group(0), "aplicado": final_text})
        return final_text
    text = pattern_fraction.sub(fraction_replacer, text)

    if modifications and logger:
        log_entry = {
            "frase_original": original_text,
            "frase_modificada": text,
            "regla_aplicada": "normalize_ranges_fractions",
            "modificaciones": modifications
        }
        logger.info(json.dumps(log_entry, ensure_ascii=False))

    return text