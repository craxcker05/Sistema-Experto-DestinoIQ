# ==========================================
# Archivo: motor.py
# Sistema Experto: Recomendador de Destinos de Viaje
# ==========================================

# ---------------------------------------------------------
# PREGUNTAS (hechos que recibe el motor)
# ---------------------------------------------------------
PREGUNTAS = [
    {"id": "clima", "pregunta": "¿Qué clima prefieres para tu viaje?", "opciones": ["Cálido", "Frío", "Templado"]},
    {"id": "entorno", "pregunta": "¿Qué tipo de entorno buscas?", "opciones": ["Playa", "Montaña", "Ciudad", "Selva/Naturaleza"]},
    {"id": "presupuesto", "pregunta": "¿Cuál es tu presupuesto estimado?", "opciones": ["Bajo (Mochilero)", "Medio (Turista)", "Alto (Lujo)"]},
    {"id": "duracion", "pregunta": "¿Cuánto durará el viaje?", "opciones": ["Fin de semana", "Una semana", "Más de una semana"]},
    {"id": "compania", "pregunta": "¿Con quién viajas?", "opciones": ["Solo", "En Pareja", "En Familia", "Con Amigos"]},
    {"id": "actividad", "pregunta": "¿Cuál es tu objetivo principal?", "opciones": ["Relajación total", "Aventura y Adrenalina", "Turismo Cultural/Histórico", "Fiesta y Vida Nocturna"]},
    {"id": "transporte", "pregunta": "¿Qué medio de transporte prefieres para llegar?", "opciones": ["Avión", "Auto / Roadtrip", "Tren / Bus"]},
    {"id": "documentacion", "pregunta": "¿Qué documentos tienes disponibles?", "opciones": ["Solo Cédula/DNI", "Pasaporte", "Pasaporte y Visas"]},
    {"id": "interes", "pregunta": "¿Qué interés secundario tienes?", "opciones": ["Gastronomía", "Compras", "Naturaleza y Paisajes", "Arte y Museos"]},
    {"id": "continente", "pregunta": "¿Tienes preferencia de continente?", "opciones": ["América", "Europa", "Asia", "África/Oceanía", "Me da igual"]},
    {"id": "idioma", "pregunta": "¿Es un problema la barrera del idioma?", "opciones": ["Sí, prefiero que hablen español", "No, hablo inglés", "No me importa usar traductor"]},
    {"id": "multitud", "pregunta": "¿Cómo prefieres el ambiente?", "opciones": ["Tranquilo y aislado", "Concurrido y turístico"]}
]

# ---------------------------------------------------------
# BASE DE CONOCIMIENTO (las reglas)
# ---------------------------------------------------------
REGLAS = [
    {
        "nombre": "Regla 1: Aventura Extrema Sur",
        "condiciones": {"clima": "Frío", "entorno": "Montaña", "actividad": "Aventura y Adrenalina", "interes": "Naturaleza y Paisajes"},
        "conclusion": "Trekking en la Patagonia (Argentina/Chile). Ideal para amantes del frío, las montañas y la aventura extrema."
    },
    {
        "nombre": "Regla 2: Paraíso Caribeño Familiar/Pareja",
        "condiciones": {"clima": "Cálido", "entorno": "Playa", "actividad": "Relajación total", "continente": "América"},
        "conclusion": "Resort All-Inclusive en Cancún o Punta Cana. Perfecto para desconectar, sol, arena y comodidades sin estrés."
    },
    {
        "nombre": "Regla 3: Inmersión Histórica Europea",
        "condiciones": {"entorno": "Ciudad", "actividad": "Turismo Cultural/Histórico", "continente": "Europa", "documentacion": "Pasaporte"},
        "conclusion": "Tour histórico por Roma y Florencia (Italia). Una inmersión profunda en arte, museos, historia antigua y excelente gastronomía."
    },
    {
        "nombre": "Regla 4: Misticismo Andino",
        "condiciones": {"entorno": "Montaña", "actividad": "Turismo Cultural/Histórico", "continente": "América", "presupuesto": "Medio (Turista)"},
        "conclusion": "Expedición a Cusco y Machu Picchu (Perú). Combina historia milenaria, paisajes montañosos y una cultura vibrante."
    },
    {
        "nombre": "Regla 5: Capital del Consumo",
        "condiciones": {"entorno": "Ciudad", "interes": "Compras", "presupuesto": "Alto (Lujo)", "documentacion": "Pasaporte y Visas"},
        "conclusion": "Nueva York (EE.UU.). El paraíso de las compras, espectáculos de Broadway y restaurantes de lujo."
    },
    {
        "nombre": "Regla 6: Desconexión Verde",
        "condiciones": {"entorno": "Selva/Naturaleza", "actividad": "Aventura y Adrenalina", "clima": "Cálido", "multitud": "Tranquilo y aislado"},
        "conclusion": "Expedición al Amazonas (Ecuador/Colombia/Brasil). Una experiencia inmersiva lejos de la civilización."
    },
    {
        "nombre": "Regla 7: Ruta Enológica Romántica",
        "condiciones": {"interes": "Gastronomía", "compania": "En Pareja", "actividad": "Relajación total", "clima": "Templado"},
        "conclusion": "Ruta del Vino en Mendoza (Argentina) o Valle de Guadalupe (México). Catas, viñedos, clima agradable y romance."
    },
    {
        "nombre": "Regla 8: Vida Nocturna Costera",
        "condiciones": {"actividad": "Fiesta y Vida Nocturna", "entorno": "Playa", "multitud": "Concurrido y turístico"},
        "conclusion": "Ibiza (España) o Miami (EE.UU.). Playas espectaculares de día y los mejores clubes del mundo por la noche."
    },
    {
        "nombre": "Regla 9: Contraste Asiático",
        "condiciones": {"continente": "Asia", "interes": "Arte y Museos", "duracion": "Más de una semana", "idioma": "No me importa usar traductor"},
        "conclusion": "Tokio y Kioto (Japón). Un viaje largo que requiere adaptación cultural, pero ofrece un choque fascinante entre tecnología y tradición."
    },
    {
        "nombre": "Regla 10: Escapada Local",
        "condiciones": {"duracion": "Fin de semana", "transporte": "Auto / Roadtrip", "presupuesto": "Bajo (Mochilero)"},
        "conclusion": "Escapada Rural a un Pueblo Mágico local. Toma el auto, alquila una cabaña económica y disfruta de un fin de semana fuera de la rutina."
    },

    # Familia A: compañía
    {
        "nombre": "Regla 11: Temáticas Familiares Americanas",
        "condiciones": {"compania": "En Familia", "entorno": "Ciudad", "continente": "América"},
        "conclusion": "Parques temáticos de Orlando (EE.UU.) o Ciudad de México con niños. Atracciones, espectáculos y planes pensados para toda la familia."
    },
    {
        "nombre": "Regla 12: Invierno Familiar en la Montaña",
        "condiciones": {"compania": "En Familia", "entorno": "Montaña", "clima": "Frío"},
        "conclusion": "Vacaciones de nieve en Bariloche (Argentina) o Andorra. Esquí, lomas de nieve y cabañas para compartir en familia."
    },
    {
        "nombre": "Regla 13: Mochilero en Solitario",
        "condiciones": {"compania": "Solo", "actividad": "Aventura y Adrenalina", "presupuesto": "Bajo (Mochilero)"},
        "conclusion": "Ruta mochilera por Nepal, India o Vietnam. Alojamientos económicos, mucha aventura y una comunidad viajera global que facilita conocer gente."
    },
    {
        "nombre": "Regla 14: Salida de Inquietos",
        "condiciones": {"compania": "Con Amigos", "actividad": "Fiesta y Vida Nocturna", "entorno": "Ciudad"},
        "conclusion": "Escapada de amigos por Berlín, Ámsterdam o Bangkok. Escena nocturna de clase mundial, hostales con ambiente y presupuestos ajustados entre todos."
    },

    # Familia B: presupuesto × continente
    {
        "nombre": "Regla 15: Europa Mochilera",
        "condiciones": {"presupuesto": "Bajo (Mochilero)", "continente": "Europa", "entorno": "Ciudad"},
        "conclusion": "Europa con mochila: Praga, Budapest y Lisboa. Ciudades con hostel barato, vida nocturna económica y mucha historia a bajo coste."
    },
    {
        "nombre": "Regla 16: Shopping de Lujo Europeo",
        "condiciones": {"presupuesto": "Alto (Lujo)", "continente": "Europa", "interes": "Compras"},
        "conclusion": "París, Londres y Milán. Boutiques de alta gama, grandes almacenes históricos y experiencias VIP de compras premium."
    },
    {
        "nombre": "Regla 17: Islas Asiáticas Económicas",
        "condiciones": {"presupuesto": "Bajo (Mochilero)", "continente": "Asia", "entorno": "Playa"},
        "conclusion": "Islas de Tailandia, Vietnam o Indonesia. Bungalows sobre el mar, comida callejera barata y playas paradisíacas con presupuesto mínimo."
    },
    {
        "nombre": "Regla 18: Costa Americana Turista",
        "condiciones": {"presupuesto": "Medio (Turista)", "continente": "América", "entorno": "Playa"},
        "conclusion": "Costa de Colombia (Cartagena) o de Brasil (Rio de Janeiro). Buena relación calidad-precio, playas cálidas y oferta turística completa."
    },

    # Familia C: transporte
    {
        "nombre": "Regla 19: Roadtrip Americano",
        "condiciones": {"transporte": "Auto / Roadtrip", "continente": "América", "actividad": "Aventura y Adrenalina"},
        "conclusion": "Ruta 40 (Argentina), Carretera Austral (Chile) o Baja California (México). Kilómetros de carretera icónicos, acampada y paisajes salvajes."
    },
    {
        "nombre": "Regla 20: Carretera Europea",
        "condiciones": {"transporte": "Auto / Roadtrip", "continente": "Europa", "clima": "Templado"},
        "conclusion": "Costa de Amalfi (Italia), Provenza (Francia) o Toscana. Conducir por rutas postales con paradas de vino, pueblos y miradores."
    },
    {
        "nombre": "Regla 21: Interrail Clásico",
        "condiciones": {"transporte": "Tren / Bus", "continente": "Europa", "actividad": "Turismo Cultural/Histórico"},
        "conclusion": "Interrail por Europa: París, Ámsterdam, Praga y Viena en tren. Viajar por el trayecto es parte del viaje cultural."
    },
    {
        "nombre": "Regla 22: Gran Tour Asiático",
        "condiciones": {"transporte": "Avión", "continente": "Asia", "duracion": "Más de una semana"},
        "conclusion": "Gran tour por Asia (Tokio, Bangkok, Singapur y Hanói). Aprovecha el vuelo largo con más de una semana para encadenar varias metrópolis."
    },

    # Familia D: documentación
    {
        "nombre": "Regla 23: Sudamérica sin Pasaporte",
        "condiciones": {"documentacion": "Solo Cédula/DNI", "continente": "América", "actividad": "Turismo Cultural/Histórico"},
        "conclusion": "Circuito por Perú, Colombia y Chile con solo cédula/DNI. Machu Picchu, Cartagena y el Atacama sin trámites de pasaporte."
    },
    {
        "nombre": "Regla 24: Caribe Cédula al Día",
        "condiciones": {"documentacion": "Solo Cédula/DNI", "continente": "América", "entorno": "Playa"},
        "conclusion": "Caribe accesible con solo cédula: Cartagena, Santa Marta o Galápagos. Playa caribeña sin necesidad de pasaporte."
    },
    {
        "nombre": "Regla 25: China con Visado",
        "condiciones": {"documentacion": "Pasaporte y Visas", "continente": "Asia", "entorno": "Ciudad"},
        "conclusion": "Gran Tour por China: Pekín, la Gran Muralla y Shanghái. Exige visado, pero tu documentación completa te lo permite."
    },
    {
        "nombre": "Regla 26: Mediterráneo con Pasaporte",
        "condiciones": {"documentacion": "Pasaporte", "continente": "Europa", "entorno": "Playa"},
        "conclusion": "Mediterráneo en Grecia o Portugal: islas griegas, Algarve y Lisboa. Con pasaporte vigente cruzas sin complicaciones."
    },

    # Familia E: idioma
    {
        "nombre": "Regla 27: Hispanofonía Urbana",
        "condiciones": {"idioma": "Sí, prefiero que hablen español", "continente": "América", "entorno": "Ciudad"},
        "conclusion": "Ciudad de México, Buenos Aires o Bogotá. Te mueves sin barrera idiomática y con una escena cultural y gastronómica riquísima."
    },
    {
        "nombre": "Regla 28: España sin Acento Raro",
        "condiciones": {"idioma": "Sí, prefiero que hablen español", "continente": "Europa", "entorno": "Ciudad"},
        "conclusion": "Andalucía, Madrid y Barcelona. Europa con el idioma de casa: tapas, arte y sol sin barreras."
    },
    {
        "nombre": "Regla 29: Mundo Anglo en Europa",
        "condiciones": {"idioma": "No, hablo inglés", "continente": "Europa", "entorno": "Ciudad"},
        "conclusion": "Londres, Dublín o Ámsterdam. Ciudades donde el inglés te lleva a todas partes y la oferta cultural es enorme."
    },

    # Familia F: multitud
    {
        "nombre": "Regla 30: Refugio de Lujo",
        "condiciones": {"multitud": "Tranquilo y aislado", "presupuesto": "Alto (Lujo)", "entorno": "Playa"},
        "conclusion": "Resort privado de lujo (Maldivas, Seychelles o Fiyi). Villas sobre el agua, playa exclusiva y cero multitudes."
    },
    {
        "nombre": "Regla 31: Grandes Capitales Culturales",
        "condiciones": {"multitud": "Concurrido y turístico", "entorno": "Ciudad", "actividad": "Turismo Cultural/Histórico"},
        "conclusion": "París o Londres en plena temporada. Museos de primer nivel y el bullicio de las ciudades más visitadas del mundo."
    },

    # Familia G: intereses cruzados
    {
        "nombre": "Regla 32: Japón Gastronómico",
        "condiciones": {"interes": "Gastronomía", "continente": "Asia", "duracion": "Más de una semana"},
        "conclusion": "Ruta gastronómica por Tokio y Osaka. Ramen de calle, sushi de Michelin y mercados centenarios con tiempo suficiente para saborearlo."
    },
    {
        "nombre": "Regla 33: Sabor Americano",
        "condiciones": {"interes": "Gastronomía", "entorno": "Ciudad", "continente": "América"},
        "conclusion": "Ciudad de México y Buenos Aires. Taquerías, parrillas y cocinas de autor: América Latina es un destino gourmet."
    },
    {
        "nombre": "Regla 34: Grandes Museos Europeos",
        "condiciones": {"interes": "Arte y Museos", "entorno": "Ciudad", "continente": "Europa"},
        "conclusion": "París (Louvre, Orsay) y Ámsterdam (Rijksmuseum, Van Gogh). Un viaje entre masterpieces y barrios artísticos."
    },
    {
        "nombre": "Regla 35: Círculo Ártico",
        "condiciones": {"interes": "Naturaleza y Paisajes", "clima": "Frío", "duracion": "Más de una semana"},
        "conclusion": "Círculo Ártico: Islandia, Noruega y Finlandia. Auroras boreales, glaciares y fiordos con más de una semana para explorarlos."
    },
    {
        "nombre": "Regla 36: Termas y Descanso Invernal",
        "condiciones": {"actividad": "Relajación total", "clima": "Frío", "entorno": "Montaña"},
        "conclusion": "Balnearios y termas de montaña (Banff, Pucón o los Andes). Aguas termales, chimenea y descanso total entre nieves."
    },
    {
        "nombre": "Regla 37: Deportes Acuáticos Tropicales",
        "condiciones": {"actividad": "Aventura y Adrenalina", "entorno": "Playa", "clima": "Cálido"},
        "conclusion": "Costa Rica o Panamá. Surf, kitesurf, buceo y puentes colgantes: aventura pura bajo el sol tropical."
    },
    {
        "nombre": "Regla 38: Fiebre del Caribe",
        "condiciones": {"actividad": "Fiesta y Vida Nocturna", "entorno": "Playa", "continente": "América"},
        "conclusion": "Cancún o Río de Janeiro. Playa de día y fiesta de playa latinoamericana por la noche."
    },
    {
        "nombre": "Regla 39: Mercados del Sudeste Asiático",
        "condiciones": {"interes": "Compras", "continente": "Asia", "presupuesto": "Bajo (Mochilero)"},
        "conclusion": "Mercados de Bangkok, Hanói y Bali. Regateo, artesanía y moda económica en los mercados más famosos de Asia."
    },

    # Familia H: África/Oceanía
    {
        "nombre": "Regla 40: Safari Africano",
        "condiciones": {"continente": "África/Oceanía", "actividad": "Aventura y Adrenalina", "interes": "Naturaleza y Paisajes"},
        "conclusion": "Safari en Kenia y Tanzania (Masái Mara, Serengueti). Los grandes cinco en su hábitat natural."
    },
    {
        "nombre": "Regla 41: Islas del Pacífico",
        "condiciones": {"continente": "África/Oceanía", "entorno": "Playa", "actividad": "Relajación total"},
        "conclusion": "Fiyi o Zanzíbar. Islas remotas, agua turquesa y el silencio perfecto para desconectar del mundo."
    }
]

# ---------------------------------------------------------
# MOTOR DE INFERENCIA
# ---------------------------------------------------------

# Respuesta "libre": cumple cualquier valor del atributo (ej. "Me da igual")
RESPUESTAS_LIBRES = {"continente": "Me da igual"}

MENSAJE_FALLBACK = (
    "Destino Explorador Libre. Tu perfil es tan único que no encaja en un paquete "
    "tradicional. Te recomendamos contactar a una agencia de viajes a medida."
)


def _coincide(hechos_usuario, clave, valor_requerido):
    """True si la respuesta cumple el valor exigido por la regla."""
    respuesta = hechos_usuario.get(clave)
    if clave in RESPUESTAS_LIBRES and respuesta == RESPUESTAS_LIBRES[clave]:
        return True
    return respuesta == valor_requerido


def _reglas_activables(hechos_usuario):
    """Reglas cuyas condiciones se cumplen al 100 %."""
    activables = []
    for regla in REGLAS:
        cumplida = all(
            _coincide(hechos_usuario, clave, valor)
            for clave, valor in regla["condiciones"].items()
        )
        if cumplida:
            activables.append(regla)
    return activables


def _resolver_conflicto(reglas_activables):
    """Regla más específica (más condiciones); en empate, la primera de la lista."""
    regla_ganadora = None
    max_condiciones = -1
    for regla in reglas_activables:
        cantidad = len(regla["condiciones"])
        if cantidad > max_condiciones:
            max_condiciones = cantidad
            regla_ganadora = regla
    return regla_ganadora


def inferir_destino(hechos_usuario):
    """Recomendación para un perfil de respuestas {"clima": "Frío", ...}."""
    activables = _reglas_activables(hechos_usuario)
    if not activables:
        return MENSAJE_FALLBACK
    return _resolver_conflicto(activables)["conclusion"]


def inferir_top(hechos_usuario, n=3):
    """Hasta n recomendaciones de mejor a peor; la primera es la de inferir_destino."""
    activables = _reglas_activables(hechos_usuario)
    if not activables:
        return [MENSAJE_FALLBACK]
    ordenadas = sorted(
        activables, key=lambda regla: len(regla["condiciones"]), reverse=True
    )
    resultado = []
    for regla in ordenadas:
        if regla["conclusion"] not in resultado:
            resultado.append(regla["conclusion"])
        if len(resultado) >= n:
            break
    return resultado


def evaluar_reglas(hechos_usuario):
    """Para cada regla, qué cumplió y qué le faltó, ordenadas de mejor a peor."""
    resultados = []
    for regla in REGLAS:
        cumplidas, faltantes = [], []
        for clave, valor in regla["condiciones"].items():
            if _coincide(hechos_usuario, clave, valor):
                detalle = ""
                if hechos_usuario.get(clave) != valor:
                    detalle = " (respondiste 'Me da igual')"
                cumplidas.append(f"{clave}: {valor}{detalle}")
            else:
                faltantes.append(f"{clave}: {valor}")
        total = len(regla["condiciones"])
        resultados.append({
            "nombre": regla["nombre"],
            "conclusion": regla["conclusion"],
            "condiciones_totales": total,
            "cumplidas": cumplidas,
            "faltantes": faltantes,
            "porcentaje": round(100 * len(cumplidas) / total),
            "activada": len(faltantes) == 0,
        })
    resultados.sort(key=lambda r: (r["activada"], r["porcentaje"]), reverse=True)
    return resultados
