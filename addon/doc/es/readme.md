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

Este complemento tiene dos formas de usar números a palabras que se detallan a continuación:

* Modo en tiempo real: mientras NVDA hable y exista texto que contenga números dentro de él, la conversión mostrará su resultado y este se transmitirá por voz. Esto, por supuesto, se aplica en cualquier sintetizador de voz que uses.
* Modo manual: puedes escribir números, texto y/o números a la vez, interactuando mediante un cuadro de diálogo que te permitirá hacerlo. La ventana de diálogo tiene:
	* Un cuadro de edición para escribir tu entrada.
	* Un botón convertir. Al presionar este botón, se te mostrará un cuadro de mensaje con el resultado final.
	* Un botón cancelar: sale del diálogo de conversión.

### Gestos de entrada:

* Alternar números a palabras (o modo en tiempo real): Gesto sin asignar por ahora para evitar interferencia con otros complementos.
* Abrir el diálogo de conversión (o modo manual): alt+shift+NVDA+n
* ¡Más características pronto!

#### Notas importantes:

* Como la librería soporta muchos idiomas, ten en cuenta que la conversión se realizará en el idioma de tu sintetizador de voz. Siendo así, el idioma de la conversión se cambia automáticamente cuando cambies el del sintetizador.
* La librería num2words puede convertir hasta 27 números seguidos. Si el texto tiene más de 27 números, lo sabrás con un pitido y un mensaje de voz indicándotelo.
* Actualmente, la verbalización de un número convertido con el cursor no está implementada y, como consecuencia, se deletreará el número convertido.

## Compilar este complemento:

Nota: este complemento depende de un submódulo, entonces:

1. Cambia el directorio a este repositorio: `cd num2words_nvda`
2. Escribe `git submodule init` y `git submodule update` en la consola para clonar el repositorio de la librería num2words que está establecido como submódulo.
3. Si no hay errores, el comando `scons` debería funcionar correctamente.

## Contacto:

Si quieres ayudar a mejorar este complemento, puedes enviar un correo a `angelitomateocedillo@gmail.com` o puedes hacer tus contribuciones en el repositorio de GitHub.

---

# Historial de cambios:

## 0.2

* Ahora el resultado de números a palabras está en mayúsculas.
* Se actualizó la librería num2words al commit `d09862790503a0ec03f3c3ffb2f70e03c41ae2f6`.

## 0.1

* Versión inicial. Es posible que encuentres algunos errores menores. Si es así, por favor házmelo saber.