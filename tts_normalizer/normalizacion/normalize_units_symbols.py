import re
import json

UNITS_SYMBOLS = {
    "€": "euros",
    "$": "dólares",
    "%": "por ciento",
    "km/h": "kilómetros por hora",
    "km": "kilómetros",
    "m²": "metros cuadrados",
    "kg": "kilogramos",
    "°C": "grados Celsius"
}

def normalize_units_symbols(text: str, logger=None) -> str:
    """
    Busca números seguidos de unidades o símbolos y verbaliza la unidad/símbolo.
    """
    original_text = text
    modifications = []

    # Usamos un truco: iteramos por las claves más largas primero para evitar
    # que "km" coincida antes que "km/h".
    sorted_keys = sorted(UNITS_SYMBOLS.keys(), key=len, reverse=True)

    for symbol, expansion in ((key, UNITS_SYMBOLS[key]) for key in sorted_keys):
        # Regex:
        # (\d[\d\.,]*)   - Captura el número que precede (grupo 1). Acepta dígitos, puntos y comas.
        # \s*            - Cero o más espacios entre el número y el símbolo.
        # (re.escape(symbol)) - El símbolo en sí (escapado por si tiene caracteres especiales).
        pattern = re.compile(r'(\d[\d\.,]*)\s*(' + re.escape(symbol) + r')(?!\w)', re.IGNORECASE)

        def unit_replacer(match):
            number_part = match.group(1)
            original_symbol = match.group(2)
            
            # Construimos el reemplazo: el número original + espacio + la expansión del símbolo.
            replacement = f"{number_part} {expansion}"
            
            modifications.append({
                "detectado": match.group(0).strip(),
                "aplicado": replacement
            })
            return replacement

        text = pattern.sub(unit_replacer, text)

    if modifications and logger:
        log_entry = {
            "frase_original": original_text,
            "frase_modificada": text,
            "regla_aplicada": "normalize_units_symbols",
            "modificaciones": modifications
        }
        logger.info(json.dumps(log_entry, ensure_ascii=False))

    return text