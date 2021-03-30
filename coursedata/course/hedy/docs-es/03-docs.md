title: "Explicación"
level: 3
---
¡Ten cuidado! En el nivel 3 hay nuevas reglas. Si quieres imprimir algo literalmente, debes colocarlo entre comillas.

# Soluciona el problema del nombre

En el nivel 2 no podíamos usar la palabra "nombre", porque ella se encontraba en uso.

Recordando el código:

* `nombre is Hedy`
* `print Entonces tu nombre is nombre`

En el nivel 2, este código imprime "Entonces tu Hedy is Hedy"

¡Pero ahora podremos solucionar esto! Puedes hacerlo poniendo comillas alrededor del texto que quieres imprimir literalmente. ¡Pruébalo!

# Piedra, papel o tijera

En el nivel 3 podemos programar el juego piedra, papel o tijera nuevamente. Pero ahora, si quieres, agregar texto a tu programa, debes hacerlo usando comillas.

* `opciones is steen, schaar, papier`
* `print 'el ganador es ' opciones at random`

Recordatorio: "random" es la palabra en inglés para "aleatorio".

# Haz los dados

En el nivel 3 puedes nuevamente crear dados. Puedes ahora armar oraciones que indican el número que sale en cada tirada.

En el caso de "Gusanitos", puedes hacerlo así (usando comillas, naturalmente):

* `opciones is 1, 2, 3, 4, 5, gusanito`
* `print 'haz tirado un ' keuzes at random`

# ¿Quien lava los platos?

También puedes mejorar el programa para determinar quien lavara los platos, usando comillas.

Puedes hacerlo de la siguiente manera:

* `personas is mama, papa, Maria, Carlos`
* `print personas at random ' lavará los platos hoy'`

# Una mejor historia

Lo que también puedes hacer es mejorar un poco tu historia dado que puedes usar la palabra "nombre" en el texto.

## Ejemplo

Esta es mi historia, ahora el personaje principal que elijas siempre viene en el lugar del nombre. Ten cuidado de poner todas las oraciones entre comillas, ¡a excepción del nombre!

* El personaje principal de esta historia is nombre
* nombre ahora camina hacia el bosque
* nombre esta un poco asustado
* Escucha sonidos raros en todas partes
* nombre teme que este sea un bosque fantasma

## Tarea

¡Ahora tú!

1. Escribe una historia corta sobre tu personaje principal.
2. Cuando aparezca el nombre de tu personaje principal, pon siempre `nombre` (ver ejemplo)
3. También puede haber oraciones en la historia que no contengan un `nombre`
4. Ahora traduce su historia al código Hedy, de la siguiente manera:

Línea 1:
* Escribe `nombre is` y detrás el nombre de tu personaje principal.

Para todas las siguientes líneas:
* Escribe `print` y luego la línea que has inventado. Pero, ¡ten cuidado! "nombre" no debe ir entre comillas, pero el resto de la oración sí.

## Ejemplo del código Hedy

* `nombre is Carlos`
* `print nombre ' ahora camina hacia el bosque'`
* `print nombre ' esta un poco asustado'`
* `print 'Escucha sonidos raros en todas partes'`
* `print nombre ' teme que este sea un bosque fantasma'`

## Una historia interactiva

Tu puedes elegir cada vez un nuevo personaje principal. Para hacer esto, cambia la primera línea de tu programa `nombre is Carlos` por `nombre is ask Cuál es el nombre del protagonista?`
Si ejecutas el programa ahora, siempre puedes elegir un nombre diferente sin cambiar el código.

## Opciones en tu historia o juego

Tu historia puede ser todavía más interesante si la haces verdaderamente interactiva. Por ejemplo, puedes elegir si en tu historia aparece un monstruo. O puedes comprobar quien fue el ganador de piedra, papel o tijera. Eso lo podrás hacer en el nivel 4.
