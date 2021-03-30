title: "Explicación"
level: 4
---
En el nivel 4 las reglas para `ask` y `print` siguen siendo las mismas. Debes solamente usar comillas para imprimir texto literalmente.

Sin embargo, hay una funcion nueva: `if`. "If" es la palabra inglesa para "si".

Aquí encontrarás nuevamente algunas tareas para poner manos a la obra.

# ¡Prohibido para tu hermanita o hermanito menor!

Cuando yo misma aprendí a programar, el primer programa que hice fue para detectar que mi hermana no usara la computadora secretamente. Ahora puedes hacer esto tú mismo de la siguiente manera:

* `nombre is ask ¿Como te llamas?`
* `if nombre is Felienne print 'ok, puedes usar la computadora' else print '¡tienes prohibida la entrada!'`

Este código comprueba que el nombre ingresado es precisamente "Felienne". Si ese es el caso, Hedy imprime la primera oración; en caso contrario, imprime la segunda.

¡Ten cuidado! Hedy comprueba el nombre exactamente, letra por letra, de manera que debes ingresarlo precisamente, incluyendo la "F" mayúscula.

# Piedra, papel o tijera

En el nivel 4 podemos nuevamente programar el juego piedra, papel o tijera, pero ahora puedes jugar contra la computadora y comprobar quien es el ganador. El programa comienza así, ¿puedes terminarlo tú?

* `tueleccion is ask ¿que eliges tu?`
* `opciones is piedra, papel, tijera`
* `eleccioncomputadora is opciones at random`
* `si eleccioncomputadora is tijera and tueleccion is papel print '¡la computadora gana!'`
* `si eleccioncomputadora es tijera and tueleccion is piedra print '¡tu ganas!'`

Recordatorio: `random` es la palabra en inglés para "aleatorio"; `and` es la palabra inglesa para "y".

# Haz los dados

En el nivel 4 puedes nuevamente crear dados, esta vez usando `if`. Por ejemplo:

* `opciones is 1, 2, 3, 4, 5, gusanito`
* `tirada is opciones at random`
* `print 'has tirado un ' worp`
* `if tirada is gusanito print 'Puedes ya dejar de tirar.' else print '¡Debes tirar los dados una vez más!'`

Tal vez prefieras crear un juego de dados que sea completamente distinto.

# ¿Quien lava los platos?

Puedes mejorar el programa para ver quien lava los platos usando `if`. Por ejemplo:

* `personas is mama, papa, Maria, Carlos`
* `lavador is mensen at random`
* `if lavador is Carlos print 'Ups, tengo que lavar los platos' else print 'por suerte no tengo que lavar los platos porque ' lavador ' los lavara'`

# Una mejor historia

Ahora puedes mejorar tu historia agregandole distintos posibles finales.

## Ejemplo

Haz una historia con dos finales, por ejemplo:

* La princesa camina por el bosque
* Ella se encuentra con un monstruo

Final feliz:

* Ella desenfunda su espada y el monstruo se va corriendo

Final triste:

* El monstruo se come a la princesa

## Tarea

¡Ahora tú!

1. Escribe una historia con dos finales.

## Código Hedy de ejemplo
* `print 'La princesa camina por el bosque'`
* `print 'Ella se encuentra con un monstruo'`
* `final is ask ¿Quieres un final feliz o un final triste?`
* `if final is feliz print 'Ella desenfunda su espada y el monstruo se va corriendo' else print 'El monstruo se come a la princesa'`

## Una historia interactiva

Puedes cambiar la historia preguntando el nombre del personaje principal. Esto funciona de la misma manera que en el nivel 3. Si combinas esto con un `if`, ¡habrás ya realizado un programa completo!

## Repetición en tu historia o juego

Lamentablemente todavía puedes tirar el dado sólo una vez, o determinar quien lavará los platos solamente una vez. Gusanitos requiere hasta ocho tiradas, ¡y tal vez quieras armar una tabla para ver quien lavará los platos cada día de la semana! A veces es muy útil si tu código puede repetirse un par de veces.

Aprenderemos cómo hacerlo en el nivel 5.
