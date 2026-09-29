# Sistema Experto - DestinoIQ

Sistema experto que recomienda destinos de viaje mediante un sistema de reglas
SI…ENTONCES y un motor de inferencia puro (sin bases de datos ni matching ponderado).

## Estructura

| Archivo | Contenido |
|---|---|
| `motor.py` | Base de conocimiento (12 atributos de perfil, 41 reglas) y motor de inferencia (`inferir_destino`, `inferir_top`, `evaluar_reglas`). |
| `app.py` | Interfaz interactiva construida con Streamlit. |
| `Presentacion_Sistema_Experto.mp4` | Video de presentación del sistema (gestionado con Git LFS). |

## Ejecución

```bash
pip install streamlit
streamlit run app.py
```

## Cómo razona el sistema

1. **Equiparación**: se comparan las respuestas del usuario con las condiciones de cada regla.
2. **Resolución de conflictos**: si se activan varias reglas, gana la más específica (más condiciones); en empate, la primera de la base.
3. **Ejecución**: se devuelve la conclusión de la regla ganadora, junto con la trazabilidad de las reglas evaluadas.

La respuesta "Me da igual" actúa como comodín: satisface cualquier valor del atributo `continente`.
