title: "Explicación"
level: 6
---

En el nivel 6 hay nuevamente elementos nuevos: ahora puedes calcular números en tu programa.

La suma es simple, lo escribes tal como lo haces en papel: por ejemplo, `5 + 5`. La multiplicación es algo distinta, porque no hay un signo de multiplicación en el teclado. Puedes buscarlo, ¡verás que no lo encuentras!

Por este motivo, realizamos la multiplicación con el asterisco (`*`). Por ejemplo: `5 * 5`. Si lees esa cuenta como "cinco veces cinco" podrás recordarla más fácilmente.

Aquí encontrarás nuevamente algunas tareas para poner manos a la obra.

# ¡Más gusanitos!

En el nivel 6 puedes nuevamente crear dados, pero esta vez puedes llevar la cuenta de cuantos puntos has acumulado en el juego.

Tal vez sepas que en el juego Gusanitos, el gussanito vale 5 puntos. Ahora puedes contar cuántos puntos llevas después de cada tirada.

Para un dado, puedes hacerlo de la siguiente manera:

1 `opciones is 1, 2, 3, 4, 5, gusanito`

2 `puntaje is 0`

3 `tirada is opciones at random`

4 `print 'has tirado un ' tirada`

5 `if tirada is gusanito puntaje is puntaje + 5 else puntaje is puntaje + tirada`

6 `print 'Tu puntaje es ' puntaje`

¿Puedes modificar el programa de manera que puedas calcular el puntaje si tiras el dado 8 veces?

Si no lo logras, puedes ver [el video de la explicación](https://www.youtube.com/watch?v=US2_w3kT47U) para ver cómo puedes modificar el programa para más dados. Nota: el video está en idioma holandés pero aún así puedes tomar ideas de allí viendo el código que escribe Felienne.

# Practicando las tablas de multiplicar

Ahora que puedes calcular, puedes crear un programa para practicar las tablas de multiplicar.

Puedes decidir que cuentas incluir, por ejemploÑ

* `respuestacorrecta is 11 * 27`
* `print 'Cuanto es 11 veces 27?'`
* `respuesta is ask Sabes la respuesta?`
* `if respuesta is respuestacorrecta print 'Bien hecho' else print 'Incorrecto! La respuesta correcta es ' respuestacorrecta`

Pero también puedes hacer que la computadora elija multiplicaciones al azar con `random`.

Entonces puedes listar algunas tablas para practicar, y elegir un número distinto para multipicarlas:

* `tablas is 4, 5, 6, 8`
* `veces is 1, 2, 3, 4, 5, 6, 7, 8, 9, 10`

* `tabla is tablas at random`
* `multiplicador is veces at random`
* `respuestacorrecta is tabla * multiplicador`

* `print 'Cuanto es ' tabla ' veces ' multiplicador '?'`

* `respuesta is ask Sabes la respuesta?`
* `if respuesta is respuestacorrecta print 'Bien hecho' else print 'Incorrecto! La respuesta correcta es ' respuestacorrecta`

# ¿Quien lava los platos? ¿Y es eso justo?

¿Cuán seguido lava los platos cada miembro de la familia? ¿Es eso justo? Ahora podemos calcularlo.

* `personas is mama, papa, Maria, Carlos`

2 `lavadoscarlos is 0`

3 `lavador is mensen at random`

4 `print lavador ' debe lavar los platos'`

5 `if lavador is Carlos lavadoscarlos is lavadoscarlos + 1`

6 `print 'Carlos lavara los platos ' lavadoscarlos ' esta semana'`

Ahora puedes copiar algunas veces las reglas 3 a 5. Por ejemplo, puedes copiarlas 7 veces para ver quien lavara los platos por una semana.

# Canta una canción con números

En las canciones, a menudo hay mucha repetición, y a veces hay números también. Por ejemplo, ¡la canción de los elefantes que se balancean!

1 `elefantes is 2`

2 `print elefantes ' se balanceaban sobre la tela de una araña'`

3 `print 'como veian que resistia, fueron a buscar otro elefante'`

4 `elefantes is elefantes + 1`

Si repites las reglas 2-4 puedes hacer que la canción continue hasta que haya muchos elefantes.

# Ya es suficiente de copiar y pegar, ¿no crees?

En el nivel 5 hemos aprendido a repetir una línea con `repeat`, por ejemplo:

* `repeat 3 times print 'Bebe Tiburon Tutududududu'`

Pero como hemos aprendido en este nivel, a veces queremos repetir varias líneas juntas. Si bien podemos hacerlo copiando y pegando, eso es mucho trabajo. En el nivel 7 aprenderemos como hacerlo de manera más fácil.
