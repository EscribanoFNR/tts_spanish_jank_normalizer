import re
import json
from num2words import num2words

def normalize_times(text: str, logger=None) -> str:
    """
    Busca y convierte formatos de hora (24h y 12h a.m./p.m.) a texto.
    """
    original_text = text
    modifications = []

    # --- Patrón 1: Formato 24h (ej: 14:30 h) ---
    pattern_24h = re.compile(r'\b(\d{1,2}):(\d{2})\s?h\b', re.IGNORECASE)

    def time_replacer_24h(match):
        hours, minutes = int(match.group(1)), int(match.group(2))
        text_hours = num2words(hours, lang='es')
        
        if minutes == 0:
            final_text = f"{text_hours} horas"
        else:
            text_minutes = num2words(minutes, lang='es')
            final_text = f"{text_hours} y {text_minutes}"

        modifications.append({"detectado": match.group(0), "aplicado": final_text})
        return final_text

    text = pattern_24h.sub(time_replacer_24h, text)

    # --- Patrón 2: Formato 12h a.m./p.m. (ej: 10:00 a.m.) ---
    # (\d{1,2}):(\d{2})\s?(a\.?m\.?|p\.?m\.?)
    # Captura hora, minutos y el indicador am/pm (con puntos opcionales).
    pattern_12h = re.compile(r'\b(\d{1,2}):(\d{2})\s?(a\.?m\.?|p\.?m\.?)\b', re.IGNORECASE)

    def time_replacer_12h(match):
        hours, minutes = int(match.group(1)), int(match.group(2))
        period = match.group(3).lower()

        text_hours = num2words(hours, lang='es')
        
        if period.startswith('a'):
            period_text = "de la mañana"
        else: # Si es p.m.
            if hours == 12:
                period_text = "del mediodía"
            elif hours >= 1 and hours < 7:
                period_text = "de la tarde"
            else: # De 7 a 11
                period_text = "de la noche"
        
        if minutes == 0:
            final_text = f"{text_hours} {period_text}"
        else:
            text_minutes = num2words(minutes, lang='es')
            final_text = f"{text_hours} y {text_minutes} {period_text}"

        modifications.append({"detectado": match.group(0), "aplicado": final_text})
        return final_text

    text = pattern_12h.sub(time_replacer_12h, text)

    if modifications and logger:
        log_entry = {
            "frase_original": original_text,
            "frase_modificada": text,
            "regla_aplicada": "normalize_times",
            "modificaciones": modifications
        }
        logger.info(json.dumps(log_entry, ensure_ascii=False))

    return text