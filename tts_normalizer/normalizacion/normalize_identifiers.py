import re
import json

def normalize_identifiers(text: str, logger=None) -> str:
    """
    Busca y normaliza formatos de contacto e identificadores como emails,
    webs y números de teléfono.
    """
    original_text = text
    modifications = []

    # --- Patrón 1: Emails ---
    # Busca un patrón típico de email. No es perfecto, pero cubre el 99% de los casos.
    email_pattern = re.compile(r'\b([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b')
    def email_replacer(match):
        user, domain = match.groups()
        domain = domain.replace('.', ' punto ')
        final_text = f"{user} arroba {domain}"
        modifications.append({"detectado": match.group(0), "aplicado": final_text})
        return final_text
    text = email_pattern.sub(email_replacer, text)

    # --- Patrón 2: Páginas Web (simplificado) ---
    web_pattern = re.compile(r'\b(www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b')
    def web_replacer(match):
        full_domain = match.group(1)
        # Reemplaza "www." por "uve doble uve doble punto" y los demás puntos
        verbalized = full_domain.replace('www.', 'uve doble uve doble punto ')
        verbalized = verbalized.replace('.', ' punto ')
        modifications.append({"detectado": full_domain, "aplicado": verbalized})
        return verbalized
    text = web_pattern.sub(web_replacer, text)

    # --- Patrón 3: Números de Teléfono (leídos dígito a dígito) ---
    # Busca secuencias de 7 a 15 dígitos que pueden contener espacios, guiones o un +.
    phone_pattern = re.compile(r'(\+?\d[\d\s-]{5,13}\d)')
    def phone_replacer(match):
        phone_str = match.group(1)
        digits_only = re.sub(r'[\s-]', '', phone_str) # Quita espacios y guiones
        
        # Deletrea cada dígito
        spelled_out = " ".join(list(digits_only))
        # Verbaliza el "+" si existe
        spelled_out = spelled_out.replace('+', 'más ')

        modifications.append({"detectado": phone_str, "aplicado": spelled_out})
        return spelled_out
    text = phone_pattern.sub(phone_replacer, text)

    if modifications and logger:
        log_entry = {
            "frase_original": original_text,
            "frase_modificada": text,
            "regla_aplicada": "normalize_identifiers",
            "modificaciones": modifications
        }
        logger.info(json.dumps(log_entry, ensure_ascii=False))

    return text