import re
import json

# Lista de acrónimos conocidos que deben ser deletreados.
# Esta lista puede crecer según las necesidades.
ACRONYMS = [
    "DNI", "IVA", "IPC", "OMS", "ONU", "OTAN", "UE", "ONG", "PYME", "CEO", "IQ"
]

def normalize_acronyms(text: str, logger=None) -> str:
    """
    Busca acrónimos de una lista predefinida y los convierte a su forma deletreada
    (ej: "OMS" -> "O, M, S").
    """
    original_text = text
    modifications = []

    for acronym in ACRONYMS:
        # Regex: Busca el acrónimo como una palabra completa (\b).
        pattern = re.compile(r'\b' + re.escape(acronym) + r'\b')

        # No usamos re.IGNORECASE aquí porque los acrónimos suelen ir en mayúsculas.
        # Si se necesitaran también en minúsculas, se añadiría el flag.

        def acronym_replacer(match):
            acronym_str = match.group(0)
            
            # Deletreamos el acrónimo separando las letras con comas y espacios.
            # Esto sugiere una pausa natural al motor TTS.
            spelled_out = ", ".join(list(acronym_str))
            
            modifications.append({
                "detectado": acronym_str,
                "aplicado": spelled_out
            })
            return spelled_out

        text = pattern.sub(acronym_replacer, text)

    if modifications and logger:
        log_entry = {
            "frase_original": original_text,
            "frase_modificada": text,
            "regla_aplicada": "normalize_acronyms",
            "modificaciones": modifications
        }
        logger.info(json.dumps(log_entry, ensure_ascii=False))

    return text
