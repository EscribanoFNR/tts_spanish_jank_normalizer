import re
import json

# El diccionario de configuración ahora está dentro del propio módulo.
ABBREVIATIONS = {
  "Sr.": "señor",
  "Sra.": "señora",
  "Srta.": "señorita",
  "Dr.": "doctor",
  "Fdez.": "Fernandez",
  "Dra.": "doctora",
  "Av.": "avenida",
  "C/": "calle",
  "nº": "número",
  "Prof.": "profesor",
  "Prof.ª": "profesora",
  "Sta.": "santa"
}

def normalize_abbreviations(text: str, logger=None) -> str:
    """
    Busca y reemplaza abreviaturas. Si se realiza algún cambio,
    registra una única entrada de log con todos los detalles.
    """
    original_text = text
    modifications = []

    for abbr, expansion in ABBREVIATIONS.items():
        # Regex mejorada:
        # \b             - Límite de palabra al inicio para asegurar que no empezamos a mitad de palabra.
        # re.escape(abbr)- La abreviatura, escapando caracteres especiales como el ".".
        # (?!\w)         - Aserción negativa: asegura que lo que sigue NO es un carácter de palabra (letra, número, _).
        #                Esto es más robusto que \b al final para abreviaturas que terminan en símbolos.
        pattern = re.compile(r'\b' + re.escape(abbr) + r'(?!\w)', re.IGNORECASE)

        # Usamos una función lambda para poder capturar qué se está reemplazando
        def replacement_handler(match):
            detected = match.group(0)
            # Guardamos el detalle de la modificación
            modifications.append({
                "detectado": detected,
                "aplicado": expansion
            })
            return expansion

        text = pattern.sub(replacement_handler, text)

    # Solo escribimos en el log SI HUBO CAMBIOS.
    if modifications and logger:
        log_entry = {
            "frase_original": original_text,
            "frase_modificada": text,
            "regla_aplicada": "normalize_abbreviations",
            "modificaciones": modifications
        }
        logger.info(json.dumps(log_entry, ensure_ascii=False))

    return text