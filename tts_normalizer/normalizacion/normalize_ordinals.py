import re
import json
from num2words import num2words

def normalize_ordinals(text: str, logger=None) -> str:
    """
    Busca y convierte números ordinales (1º, 2ª, 3er) a su forma textual,
    manejando género y la forma apocopada (apócope).
    """
    original_text = text
    modifications = []

    # La regex sigue siendo correcta
    pattern = re.compile(r'\b(\d+)(º|ª|er|do|to)\b', re.IGNORECASE)

    def ordinal_replacer(match):
        number_str = match.group(1)
        suffix = match.group(2).lower()
        
        number_int = int(number_str)
        
        # --- LÓGICA CORREGIDA ---
        
        # 1. Obtener siempre la forma masculina por defecto (sin 'gender')
        text_ordinal = num2words(number_int, to='ordinal', lang='es')

        # 2. Ajustar para el género femenino si es necesario
        if suffix == 'ª' and text_ordinal.endswith('o'):
            text_ordinal = text_ordinal[:-1] + 'a'

        # 3. Ajustar para la apócope (primer, tercer)
        if suffix == 'er':
            if text_ordinal == 'primero':
                text_ordinal = 'primer'
            elif text_ordinal == 'tercero':
                text_ordinal = 'tercer'
        
        # --- FIN DE LA CORRECCIÓN ---

        modifications.append({
            "detectado": match.group(0),
            "aplicado": text_ordinal
        })
        return text_ordinal

    processed_text = pattern.sub(ordinal_replacer, text)

    if modifications and logger:
        log_entry = {
            "frase_original": original_text,
            "frase_modificada": processed_text,
            "regla_aplicada": "normalize_ordinals",
            "modificaciones": modifications
        }
        logger.info(json.dumps(log_entry, ensure_ascii=False))

    return processed_text