import re
import json

# El diccionario de configuración ahora está dentro del propio módulo.
ABBREVIATIONS = {
"Sr.": "señor",
"Sra.": "señora",
"Srta.": "señorita",
"D.": "don",
"Da.": "doña",
"Dr.": "doctor",
"Dra.": "doctora",
"Prof.": "profesor",
"Prof.ª": "profesora",
"Mtro.": "maestro",
"Mtra.": "maestra",
"Lic.": "licenciado",
"Licda.": "licenciada",
"Ing.": "ingeniero",
"Ing.ª": "ingeniera",
"Sto.": "santo",
"Sta.": "santa",
"Pdte.": "presidente",
"Pta.": "presidenta",
"Gral.": "general",
"Alte.": "almirante",
"Cnel.": "coronel",
"Cap.": "capitán",
"Ten.": "teniente",
"Cmdte.": "comandante",
"Mr.": "míster",
"Msr.": "misis",
"Rvd.": "reverendo",
"Rda.": "reverenda",
"Av.": "avenida",
"Avda.": "avenida",
"C/": "calle",
"Cl.": "calle",
"P.º": "paseo",
"Ps.": "paseo",
"Pl.": "plaza",
"Pza.": "plaza",
"Ctra.": "carretera",
"Cam.": "camino",
"Urb.": "urbanización",
"Bloque": "bloque",
"Edif.": "edificio",
"Piso": "piso",
"Puerta": "puerta",
"nº": "número",
"núm.": "número",
"Admón.": "administración",
"Apdo.": "apartado",
"Art.": "artículo",
"Ayto.": "ayuntamiento",
"C.P.": "código postal",
"CC.AA.": "comunidades autónomas",
"Dto.": "descuento",
"EE. UU.": "Estados Unidos",
"E.U.A.": "Estados Unidos de América",
"R.U.": "Reino Unido",
"U.E.": "Unión Europea",
"U.S.A.": "United States of America",
"IVA": "impuesto sobre el valor añadido",
"Pág.": "página",
"Págs.": "páginas",
"Vol.": "volumen",
"Cap.": "capítulo",
"Tel.": "teléfono",
"Tfn.": "teléfono",
"Fax": "fax",
"Cta.": "cuenta",
"Ref.": "referencia",
"min.": "minuto",
"a.C.": "antes de Cristo",
"d.C.": "después de Cristo",
"lun.": "lunes",
"mar.": "martes",
"miér.": "miércoles",
"jue.": "jueves",
"vier.": "viernes",
"sáb.": "sábado",
"dom.": "domingo",
"ene.": "enero",
"feb.": "febrero",
"mar.": "marzo",
"abr.": "abril",
"may.": "mayo",
"jun.": "junio",
"jul.": "julio",
"ago.": "agosto",
"sept.": "septiembre",
"set.": "setiembre",
"oct.": "octubre",
"nov.": "noviembre",
"dic.": "diciembre",
"aprox.": "aproximadamente",
"máx.": "máximo",
"mín.": "mínimo",
"núm.": "número",
"ptas.": "pesetas",
"a.m.": "ante meridiem",
"p.m.": "post meridiem",
"admón.": "administración",
"arq.": "arquitecto",
"atte.": "atentamente",
"Bco.": "banco",
"Bibl.": "biblioteca",
"bro.": "hermano (brother)",
"cía.": "compañía",
"col.": "columna",
"coord.": "coordinador",
"dep.": "departamento",
"dir.": "dirección",
"edit.": "editorial",
"esq.": "esquina",
"f.c.": "ferrocarril",
"fasc.": "fascículo",
"fig.": "figura",
"fil.": "filología",
"izq.": "izquierda",
"izqda.": "izquierda",
"jul.": "juliano",
"ob.": "óbito",
"párr.": "párrafo",
"p.ej.": "por ejemplo",
"q.e.p.d.": "que en paz descanse",
"rte.": "remitente",
"sig.": "siguiente",
"ss.": "siguientes",
"ss. ss.": "según se",
"tam.": "tamaño",
"telf.": "teléfono",
"tv.": "televisión",
"v.": "véase",
"vid.": "véase",
"vol.": "volumen",
"vto.": "vuelto",
"dcha.": "derecha"
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