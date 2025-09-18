import re
import json
from num2words import num2words

def normalize_times(text: str, logger=None) -> str:
    original_text = text
    modifications = []

    # --- Patrón 1: Formato 24h (sin cambios) ---
    pattern_24h = re.compile(r'\b(\d{1,2}):(\d{2})\s?h\b', re.IGNORECASE)
    def time_replacer_24h(match):
        hours, minutes = int(match.group(1)), int(match.group(2))
        text_hours = num2words(hours, lang='es')
        if minutes == 0: final_text = f"{text_hours} horas"
        else: final_text = f"{text_hours} y {num2words(minutes, lang='es')}"
        modifications.append({"detectado": match.group(0), "aplicado": final_text})
        return final_text
    text = pattern_24h.sub(time_replacer_24h, text)

    # --- Patrón 2: Formato 12h a.m./p.m. (CON REGEX CORREGIDA) ---
    # La clave es a\.?\s?m\.? que permite un espacio opcional entre a. y m.
    pattern_12h = re.compile(r'\b(\d{1,2}):(\d{2})\s?(a\.?\s?m\.?|p\.?\s?m\.?)(?!\w)', re.IGNORECASE)
    def time_replacer_12h(match):
        hours, minutes = int(match.group(1)), int(match.group(2))
        period = match.group(3).lower().replace(" ", "").replace(".", "") # Limpiamos para tener 'am' o 'pm'
        text_hours = num2words(hours, lang='es')
        period_text = ""
        if period == 'am': period_text = "de la mañana"
        else: # es pm
            if hours == 12: period_text = "del mediodía"
            elif hours >= 1 and hours < 7: period_text = "de la tarde"
            else: period_text = "de la noche"
        if minutes == 0: final_text = f"{text_hours} {period_text}"
        else: final_text = f"{text_hours} y {num2words(minutes, lang='es')} {period_text}"
        modifications.append({"detectado": match.group(0), "aplicado": final_text})
        return final_text
    text = pattern_12h.sub(time_replacer_12h, text)

    if modifications and logger:
        log_entry = {
            "frase_original": original_text, "frase_modificada": text,
            "regla_aplicada": "normalize_times", "modificaciones": modifications
        }
        logger.info(json.dumps(log_entry, ensure_ascii=False))
    return text