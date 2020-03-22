# Piedra, papel o tijera

En el Nivel 2 podemos hacer algo nuevo, es decir, ingresar listas y elegir cosas de ellas.
Por ejemplo, puedes hacer tu propio juego de piedra, papel o tijera.

Así es como lo haces:

* `opciones is piedra, papel, tijera`
* `print opciones at random`

Random es la palabra en inglés que significa aleaorio. 

# Tira los dados

También puedes hacer un dado. Echa un vistazo a los juegos que tienes en tu armario en casa.

Así es como lo haces:

* `opciones is 1, 2, 3, 4, 5, 6`
* `print opciones at random`

Puedes crear tu propio dado? Por ejemplo el dado de la imagen?
![Un dado del juego "Gusanitos" con 1 hasta 5 y el gusanito](https://cdn.anyfinder.eu/assets/5b64147d2864c61f08bdd4fb85c70d4d26e2b8d7774dc20edabeb13c9391c327?output=webp "Gusanitos")

# ¿Quién lava los platos?

Es posible que quieras dejar que el computador elija honestamente quién debe lavar los platos o cambiar la caja de arena hoy.

¡También puedes programar esto ahora!

Así es como lo haces:

* `personas is mama, papa, Maria, Carlos`
* `print personas at random`

# Una mejor historia

Lo que ahora puedes hacer es que tu histora sea más divertida, porque el nombre de tu personaje principal ahora
debe estar en todas partes de la oración.
Tienes que programar un poco más para esto.

### Ejemplo

Esta es mi historia, ahora el personaje principal que elijas siempre viene en el lugar del nombre.

* El personaje principal de esta historia is nombre
* nombre ahora camina hacia el bosque
* nombre esta un poco asustado
* Escucha sonidos raros en todas partes
* nombre teme que este sea un bosque fantasma

### Tarea

¡Ahora tú!

1. Escribe una historia corta sobre tu personaje principal.
2. Cuando aparezca el nombre de tu personaje principal, pon siempre `nombre` (ver ejemplo)
3. También puede haber oraciones en la historia que no contengan un `nombre`
4. Ahora traduzca su historia al código Hedy. Así es como:

Línea 1:
* Escribe `nombre is` y detrás el nombre de tu personaje principal.

Para todas las siguientes líneas:
* Escribe `print` y luego la línea que has inventado. 

### Ejemplo del código Hedy
* `nombre is Carlos`
* `print nombre ahora camina hacia el bosque`
* `print nombre esta un poco asustado`
* `print Escucha sonidos raros en todas partes`
* `print nombre teme que este sea un bosque fantasma`

### Una historia interactiva

Tu puedes elegir cada vez un nuevo personaje principal. Para hacer esto, cambia la primera línea de tu programa `nombre is Carlos` por `nombre is ask Cuál es el nombre del protagonista?`
Si ejecutas el programa ahora, siempre puede elegir un nombre diferente sin cambiar el código.

### ¡Ahora hay un pequeño problema...!

¿Intentaste hacer una oración que tuviera la palabra nombre? Por ejemplo `print Mi nombre es nombre`.
Pruébalo si aún no lo has hecho.
¡Esto no funciona bien! El resultado que obtienes es: Mi Carlos es Carlos. Esto lo puedes resolver en el nivel 3. 
Haga clik en el botón "Ir al nivel 3" cuando hayas completado estas tres tareas.