# [Números a palabras](https://github.com/savoirfairelinux/num2words) para NVDA

Autor: Mateo Cedillo

## Introducción:

Me inspiré en hacer este pequeño complemento, pues muchos sintetizadores de voz como ETI-Eloquence tienen ciertos defectos en cuanto al procesamiento de números. Por ejemplo, si se tiene dos números separados por espacios y el sintetizador lo interpreta erróneamente como si de un punto decimal se tratara.

Este complemento mejora la lectura de números a palabras para estos casos, soporta números grandes y, además, la librería con la que depende admite muchos idiomas.

## comparación de resultados entre una entrada de voz original y una convertida

Esta tabla de comparación demuestra las diferencias del procesamiento de números en un sintetizador con el procesamiento de num2words.

La siguiente comparación ha sido evaluada utilizando el [controlador IBMTTS](https://github.com/davidacm/NVDA-IBMTTS-Driver) para NVDA.


### Usando números largos:

| Idioma | entrada original | Texto de salida | Entrada convertida |
|---|---|---|---|
| Español | 921359131290481307233416326 | nueve dos ún tres cinco nueve ún tres ún dos nueve cero cuatro ocho ún tres cero siete dos tres tres cuatro ún seis tres dos seis | novecientos veintiuno cuatrillones trescientos cincuenta y nueve mil ciento treinta y uno trillones doscientos noventa mil cuatrocientos ochenta y uno billones trescientos siete mil doscientos treinta y tres millones cuatrocientos dieciséis mil trescientos veintiséis |
| Inglés | 921359131290481307233416326 | nine two one three five nine one three one two nine zero four eight one three zero seven two three three four one six three two six | nine hundred and twenty-one septillion, three hundred and fifty-nine sextillion, one hundred and thirty-one quintillion, two hundred and ninety quadrillion, four hundred and eighty-one trillion, three hundred and seven billion, two hundred and thirty-three million, four hundred and sixteen thousand, three hundred and twenty-six |

### Usando espacios como separadores (en Español solamente):

* entrada original: 12 499
* Salida: doce mil cuatrocientos noventa y nueve
* Entrada convertida: doce cuatrocientos noventa y nueve

## Uso:

Este complemento tiene tres formas de usar números a palabras que se detallan a continuación:

* Modo en tiempo real: mientras NVDA hable y exista texto que contenga números dentro de él, la conversión mostrará su resultado y este se transmitirá por voz. Esto, por supuesto, se aplica en cualquier sintetizador de voz que uses.
	* Puedes usar esta característica de forma temporal agregando un gesto de entrada (ver más abajo). Siendo una característica temporal, se desactivará cuando sales de NVDA.
	* También puedes configurar esta característica para que se ponga en marcha cuando se inicie NVDA. Para hacer esto, pulsa NVDA+N, ve a `preferencias>opciones...` y selecciona la categoría número a palabras. Dentro de esta, encontrarás la casilla correspondiente.
* Modo manual: puedes escribir números, texto y/o números a la vez, interactuando mediante un cuadro de diálogo que te permitirá hacerlo. La ventana de diálogo tiene:
	* Una casilla de verificación para convertir a ordinal.
	* Si la casilla de ordinal no está activada, aparecerá un cuadro combinado para elegir el modo de conversión. Hay seis modos de conversión y son los siguientes:
		* Ordinales, por ejemplo: 1 = primero.
		* Números ordinales, por ejemplo: 1 = primero (se aplica el mismo método que la opción para ordinales).
		* Fecha, por ejemplo (en formato dd/mm/aaaa): 23/07/2023 = Veintitrés de julio de dos mil veintitrés.
		* Hora, por ejemplo: 12:30:15 = Son las doce horas, treinta minutos y quince segundos.
		* Año, por ejemplo: 1980 = mil novecientos ochenta (no tiene efecto en muchos idiomas).
		* Moneda, por ejemplo: 2.15 = dos euros con quince céntimos.
			* Una vez que selecciones esta opción, aparecerá un nuevo cuadro combinado para elegir la moneda. Cada idioma tiene monedas diferentes además del euro, y la lista puede variar.
	* Un cuadro de edición para escribir tu entrada.
	* Un botón convertir. Al presionar este botón, se te mostrará un cuadro de mensaje con el resultado final.
	* Un botón cancelar: sale del diálogo de conversión.
* Modo de selección: si hay un texto seleccionado que contiene números o números entre palabras, el resultado se convertirá y se pronunciará en voz alta.

Nota: también puedes copiar el último resultado que se haya convertido (ver más abajo)

### Gestos de entrada:

* Alternar números a palabras (o modo en tiempo real): Gesto sin asignar por ahora para evitar interferencia con otros complementos.
* Convertir números en palabras basado en el texto seleccionado (modo de selección): gesto sin asignar.
* Abrir el diálogo de conversión (o modo manual): alt+shift+NVDA+n
* Copiar el último resultado hablado: gesto sin asignar.
* ¡Más características pronto!

#### Notas importantes:

* Como la librería soporta muchos idiomas, ten en cuenta que la conversión se realizará en el idioma de tu sintetizador de voz. Siendo así, el idioma de la conversión se cambia automáticamente cuando cambies el del sintetizador.
* Al iniciar NVDA, se comprueba el idioma de tu sintetizador. Si este no es compatible, se te avisará.
* La librería num2words puede convertir hasta 27 números seguidos. Si el texto tiene más de 27 números, lo sabrás con un pitido y un mensaje de voz indicándotelo.
* Actualmente, la verbalización de un número convertido con el cursor no está implementada y, como consecuencia, se deletreará el número convertido.

## Compilar este complemento:

Nota: este complemento depende de un submódulo, entonces:

1. Cambia el directorio a este repositorio: `cd num2words_nvda`
2. Escribe `git submodule init` y `git submodule update` en la consola para clonar el repositorio de la librería num2words que está establecido como submódulo.
3. Si no hay errores, el comando `scons` debería funcionar correctamente.

## Complemento(s) en los que me inspiré

Durante en el desarrollo de este complemento, me he inspirado en los siguientes los cuales agradezco a cada uno de los autores de estos complementos:

* [Reloj y calendario para NVDA](https://addons.nvda-project.org/addons/clock.en.html) porque me dio una idea base de cómo podría implementar la conversión de fecha y hora.

## Contacto:

Si quieres ayudar a mejorar este complemento, puedes enviar un correo a `angelitomateocedillo@gmail.com` o puedes hacer tus contribuciones en el repositorio de GitHub.

---

# Historial de cambios:

## 0.5.1

* En este parche arreglé un error con el modo de conversión manual, debido a las consecuencias de la reorganización del código.

## 0.5

* Agregado: Se ha reintroducido la compatibilidad con NVDA 2024.1, agregando compatibilidad con el modo de voz en petición para alternar num2words en tiempo real.
* Agregado: nuevos comandos
	* Convierte números en palabras basado en el texto seleccionado.
	* Copiar el último resultado convertido, gracias `mk360`.
* Corregido: errores con decimales no válidos. Ahora, por ejemplo, cuando num2words en tiempo real está activado, NVDA no se quedará callado ni mostrará un error en el log en estos casos.
* Actualizado: libraría num2words.
	* Esta actualización tiene nuevos idiomas: Español Costa Rica, galés y checheno
	* Mejoras de código, compativilidad con python 3.12.
* Se hizo una refactorización de código a todo el complemento. De esta forma, puede ser más legible y organizado para los contribuyentes.

## 0.4.1

* En este parche hice una regresión a la última versión de NVDA probada. Aunque prefiero ser honesto y la cuestión es que probé este complemento con las alpha de 2024.1 y 2024.1 aún no se ha lanzado, para evitar problemas al publicarlo en la tienda de complementos, regresaré con gusto a 2023.3 como la última versión probada.
* Además, se han aclarado las variables en algunas funciones del código para mejorar la legibilidad.

## 0.4

* Ahora, al seleccionar el modo de conversión por moneda, se agregó un cuadro combinado para seleccionar la moneda a ser convertida, a través de una lista de monedas que soporta el idioma seleccionado y determinado por el sintetizador.
* Se agregó una opción en el panel de opciones de NVDA para activar la lectura de números a palabras en tiempo real al iniciar.
* Se agregó el idioma Ucraniano, gracias a `Георгій` y `Володимир Пиріг`.
* Actualizado num2words a 0.5.13
	* Agrega soporte para bielorruso y eslovaco.
	* Actualizaciones y refactorizaciones de código para el ruso y ucraniano.
* El complemento ya no revisa si la opción scratchpad en el `panel de opciones > avanzado` está activada.
* Arreglado: error `string index out of range` al navegar por sitios web. Gracias, `Volodymyr`.
* Arreglado: La conversión en tiempo real y los separadores de voz de NVDA. El complemento ahora debería separar las palabras convertidas correctamente.
* Arreglado: compatibilidad con NVDA 2024.1.
* Arreglado: manejo inadecuado de la traducción en la conversión por hora. Los mantenedores de idiomas deberán actualizar las nuevas entradas para que la característica funcione correctamente.
* Ordenado el código para una mejor legibilidad.

## 0.3

* Agregado idioma Turco, gracias a `Umut KORKMAZ`.
* Se agregó la conversión de fecha y hora en la ventana de conversiones de forma manual.

## 0.2

* Ahora el resultado de números a palabras está en mayúsculas.
* Se actualizó la librería num2words al commit `da48a319179f19b900d5b01ed394b304e94d31cf`.
* Se agregaron los modos de conversión soportados por la librería num2words en la interfaz de conversión manual.
* Correcciones menores en la interfaz de conversión manual.
* Se agregó la comprobación de verificación del idioma del sintetizador al iniciar NVDA. Entonces, en caso de que el idioma no se soporte, se deshabilitará una parte del complemento.

## 0.1

* Versión inicial. Es posible que encuentres algunos errores menores. Si es así, por favor házmelo saber.