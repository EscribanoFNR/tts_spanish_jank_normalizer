import re
import json

UNITS_SYMBOLS = {
    "€": "euros", "$": "dólares", "USD": "dólares", "%": "por ciento",
    "km/h": "kilómetros por hora", "km": "kilómetros", "m²": "metros cuadrados", "kWh": "Kilo vatios hora","kW": "Kilo vatios",
    "kg": "kilogramos", "mg": "miligramos", "°C": "grados Celsius", "Hijos/Mujer": "Hijos por Mujer",
    "s": "segundos", "$/barril": "dólares por barril", "dolares/barril": "dólares por barril", "dólares/barril": "dólares por barril"
}
def normalize_units_symbols(text: str, logger=None) -> str:
    original_text = text
    modifications = []

    # --- 1. Regla basada en diccionario (CON REGEX CORREGIDA) ---
    sorted_keys = sorted(UNITS_SYMBOLS.keys(), key=len, reverse=True)
    for symbol, expansion in ((key, UNITS_SYMBOLS[key]) for key in sorted_keys):
        # Esta regex ahora sí captura correctamente números negativos antes de un símbolo.
        pattern = re.compile(r'(?<!\w)(-?\d[\d\.,]*)\s*(' + re.escape(symbol) + r')(?!\w)', re.IGNORECASE)
        def unit_replacer(match):
            number_part, original_symbol = match.groups()
            replacement = f"{number_part} {expansion}"
            modifications.append({"detectado": match.group(0).strip(), "aplicado": replacement})
            return replacement
        text = pattern.sub(unit_replacer, text)

    # --- 2. Regla para horas sueltas (sin cambios) ---
    pattern_hours = re.compile(r'\b(\d+)\s+(h)\b', re.IGNORECASE)
    def hour_replacer(match):
        number_part, h_symbol = match.groups()
        replacement = f"{number_part} horas"
        modifications.append({"detectado": match.group(0), "aplicado": replacement})
        return replacement
    text = pattern_hours.sub(hour_replacer, text)

    # --- 3. Regla para barras genéricas (sin cambios) ---
    pattern_slash = re.compile(r'\b([a-zA-Záéíóúñ]+)\/([a-zA-Záéíóúñ]+)\b', re.IGNORECASE)
    def slash_replacer(match):
        word1, word2 = match.groups()
        replacement = f"{word1} por {word2}"
        modifications.append({"detectado": match.group(0), "aplicado": replacement})
        return replacement
    text = pattern_slash.sub(slash_replacer, text)

    if modifications and logger:
        log_entry = {
            "frase_original": original_text, "frase_modificada": text,
            "regla_aplicada": "normalize_units_symbols", "modificaciones": modifications
        }
        logger.info(json.dumps(log_entry, ensure_ascii=False))
    return text