import re
import json
from num2words import num2words

# Lista de palabras clave que suelen preceder a un número romano.
ROMAN_CONTEXT_WORDS = [
    "Siglo", "Capítulo", "Tomo", "Volumen", "Rey", "Reina", "Papa",
    "Juan Carlos", "Felipe", "Alfonso", "Luis"
]

def roman_to_int(s: str) -> int:
    # ... (la función roman_to_int no cambia)
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    i=0; num=0
    while i < len(s):
        if i+1<len(s) and roman_map[s[i]] < roman_map[s[i+1]]:
            num+=roman_map[s[i+1]]-roman_map[s[i]]; i+=2
        else:
            num+=roman_map[s[i]]; i+=1
    return num

def normalize_roman_numerals(text: str, logger=None) -> str:
    """
    Busca números romanos que siguen a palabras clave contextuales y los convierte a texto.
    """
    original_text = text
    modifications = []

    # --- REGEX CORREGIDA BASADA EN CONTEXTO ---
    # (\b(?:...)\s+) - Captura (grupo 1) una de las palabras clave de la lista,
    #                  seguida de uno o más espacios. (?:) es un grupo sin captura.
    # ([MDCLXVI]+)\b   - Captura (grupo 2) el número romano como una palabra completa.
    context_pattern = '|'.join(ROMAN_CONTEXT_WORDS)
    pattern = re.compile(r'(\b(?:' + context_pattern + r')\s+)([MDCLXVI]+)\b', re.IGNORECASE)
    
    def roman_replacer(match):
        context_word_with_space = match.group(1) # "Siglo "
        roman_str = match.group(2).upper()
        
        number_int = roman_to_int(roman_str)
        text_number = num2words(number_int, lang='es')
        
        # Reconstruimos la frase manteniendo la palabra de contexto original
        replacement = f"{context_word_with_space}{text_number}"

        modifications.append({
            "detectado": match.group(0),
            "aplicado": replacement
        })
        return replacement

    processed_text = pattern.sub(roman_replacer, text)

    if modifications and logger:
        log_entry = {
            "frase_original": original_text,
            "frase_modificada": processed_text,
            "regla_aplicada": "normalize_roman_numerals",
            "modificaciones": modifications
        }
        logger.info(json.dumps(log_entry, ensure_ascii=False))

    return processed_text