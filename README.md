# Creador de Horarios 

Utiliza este sencillo script de python para encontrar un horario que se
adapte a tus necesidades.


## Instrucciones
---
1. Asegúrate de contar con python 3. [Descargalo aquí](https://www.python.org/downloads/)  
2. Instala los paquetes prettytable con pip  
* **Para windows**  
Abrir PowerShell o cmd como administrador.  
    <pre><code>pip3 install prettytable</pre></code>
* **Para GNU/Linux**  
    <pre><code>$ sudo pip3 install --user prettytable </pre></code>

3. Descarga este repositorio como zip
 
4. Extraer

5. Cambiar directorio a carpeta de extracción

6. Cambiar las configuraciones del archivo ***configuracion.json***

7.  Correr script con el comando  
    <pre><code>python3 -m main</pre></code>


## Configuración del archivo JSON ##
---
Para configurar las opciones, es necesario  modificar el archivo
***configuracion.json*** con los siguientes parámetros:

   * *licenciatura*: "ICO"

   * *candidatos*: Lista de UA de entre las cuales te gustaría elegir.
    *ej:["L41006", "L41035", ...]*

   * *num_cursar*: Número de clases a las que te gustaría asistir este semestre.  
   **Ojo:** Tiene que ser menor o igual al número de candidatos.

   * *prioridad* (opcional): Materia con un profesor u horario en específico que es imprescindible en tu horario. Elegir un solo valor numérico 1-138 de la columna "num" del archivo recursos/plantilla_ico_2020A.csv o "" (cadena vacía) si ningun horario es vital para tí.  
   *ej.:* "3", "22", ""

## Notas ##
   * Se recomienda agregar una materia prioridad, ya que esto reduce el criterio de búsqueda.
   * El parámetro *num_cursar* es un **entero** y el parámetro prioridad es una **cadena**.
   * El parámetro *num_cursar* puede ser menor o igual al número de materias que proveas como opción.


# IMPORTANTE #
**No modificar ni mover de lugar ninguno de los archivos .csv**


### Autor ###

**Carlos Carral C.** 
<br>Correo: carloscarral13@gmail.com
