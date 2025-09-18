import re
import json
from num2words import num2words

def normalize_numbers(text: str, logger=None) -> str:
    original_text = text
    modifications = []

    # --- REGEX CORREGIDA ---
    # Usamos lookbehind negativo para evitar que el signo negativo sea parte de otra palabra
    pattern = re.compile(r'(?<!\w)(-?\d{1,3}(\.\d{3})*(,\d+)?)(?!\w)')

    def number_replacer(match):
        number_str = match.group(1)
        
        # Limpiamos los puntos de millares
        cleaned_number_str = number_str.replace('.', '')
        
        # Verificamos si es negativo
        is_negative = cleaned_number_str.startswith('-')
        if is_negative:
            cleaned_number_str = cleaned_number_str[1:]  # Eliminamos el signo negativo

        if ',' in cleaned_number_str:
            integer_part, decimal_part = cleaned_number_str.split(',')
            # Convertimos la parte entera
            text_integer = num2words(int(integer_part), lang='es')
            # Convertimos la parte decimal
            text_decimal = num2words(int(decimal_part), lang='es')
            # Si es negativo, añadimos "menos"
            if is_negative:
                final_text = f"menos {text_integer} coma {text_decimal}"
            else:
                final_text = f"{text_integer} coma {text_decimal}"
        else:
            # Convertimos el número entero
            num_int = int(cleaned_number_str)
            text_number = num2words(num_int, lang='es')
            if is_negative:
                final_text = f"menos {text_number}"
            else:
                final_text = text_number

        modifications.append({"detectado": number_str, "aplicado": final_text})
        return final_text

    processed_text = pattern.sub(number_replacer, text)

    if modifications and logger:
        log_entry = {
            "frase_original": original_text, "frase_modificada": processed_text,
            "regla_aplicada": "normalize_numbers", "modificaciones": modifications
        }
        logger.info(json.dumps(log_entry, ensure_ascii=False))

    return processed_text