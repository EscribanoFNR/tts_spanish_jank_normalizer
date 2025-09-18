import re
import json
from num2words import num2words

def normalize_numbers(text: str, logger=None) -> str:
    """
    Busca y convierte números a su representación textual.
    - Maneja separadores de miles (puntos).
    - Maneja separadores decimales (comas).
    - Registra una única entrada de log si se realizan cambios.
    """
    original_text = text
    modifications = []

    # Explicación de la Regex:
    # \b                   - Límite de palabra al inicio para no coger números que son parte de otra palabra.
    # \d{1,3}              - Un grupo de 1 a 3 dígitos para empezar.
    # (\.\d{3})*           - Cero o más grupos de (punto seguido de 3 dígitos). Esto captura los separadores de miles.
    # (,\d+)?              - Un grupo opcional de (coma seguida de 1 o más dígitos). Esto captura la parte decimal.
    # (?!\w)               - Aserción: lo que sigue no es un carácter de palabra, para no cortar un número más largo.
    pattern = re.compile(r'\b\d{1,3}(\.\d{3})*(,\d+)?(?!\w)')

    def number_replacer(match):
        number_str = match.group(0)
        
        # Eliminar los puntos de miles
        cleaned_number_str = number_str.replace('.', '')

        # Comprobar si hay parte decimal
        if ',' in cleaned_number_str:
            integer_part, decimal_part = cleaned_number_str.split(',')
            # Convertir ambas partes a texto
            text_integer = num2words(int(integer_part), lang='es')
            text_decimal = num2words(int(decimal_part), lang='es')
            # Unirlas con "coma"
            final_text = f"{text_integer} coma {text_decimal}"
        else:
            # Si no hay decimales, solo convertir la parte entera
            final_text = num2words(int(cleaned_number_str), lang='es')

        modifications.append({
            "detectado": number_str,
            "aplicado": final_text
        })
        return final_text

    processed_text = pattern.sub(number_replacer, text)

    # Solo escribimos en el log si hubo cambios.
    if modifications and logger:
        log_entry = {
            "frase_original": original_text,
            "frase_modificada": processed_text,
            "regla_aplicada": "normalize_numbers",
            "modificaciones": modifications
        }
        logger.info(json.dumps(log_entry, ensure_ascii=False))

    return processed_text