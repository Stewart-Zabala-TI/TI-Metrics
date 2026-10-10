## Registro de Prompt # [1]

* **Fecha:** 2026-10-09

* **Módulo/Función:** data/logs.csv y data/events.json

* **Prompt Enviado:** "Actúa como ingeniero backend. Para el desarrollo de una herramienta en Python, genera dos conjuntos de datos de prueba pequeños: un archivo csv con columnas timestamp, ip, metodo, status, endpoint y un archivo json con eventos de infraestructura. Incluye todos los casos para atrapar los posibles errores que me puede dar el código."

* **Respuesta de la IA:** Proporcionó un archivo `logs.csv` y un `events.json` que incluyen intencionalmente casos trampa y datos no estructurados.

* **Análisis Crítico:** Registros con código HTTP `500` para poner a prueba la extracción limpia de IPs críticas.

* **Solución Final Aplicada:** Validé y guardé estos archivos sintéticos en la carpeta `data/` (`data/logs.csv` y `data/events.json`) para utilizarlos como el entorno de prueba oficial con el que construiré el módulo.


## Registro de Prompt # [2]

* **Fecha:** 2026-10-09

* **Módulo/Función:** src/limpieza.py

* **Prompt Enviado:** "Actúa como un desarrollador backend senior en Python. Revisa mi función cargar_y_deduplicar_logs en src/limpieza.py y contrástala con el archivo data/logs.csv. Inspecciona si mi lógica actual tiene fallos, huecos o casos borde sin cubrir, así como mal manejo de excepciones o código redundante."

* **Respuesta de la IA:** La IA sugirió refactorizar el código dividiendo la validación en funciones auxiliares independientes (`limpiar_ip` y `limpiar_status`) para seguir el principio de responsabilidad única. Sugirió verificar manualmente que la IP contenga 4 octetos numéricos válidos.

* **Análisis Crítico:** Al evaluar la sugerencia, noté que separar la validación en funciones pequeñas facilita la lectura del código y simplifica su explicación en la defensa oral. Decidí implementar la limpieza de IP comprobando manualmente las 4 partes con `.split(".")` y un bucle `for` para asegurar octetos de 0 a 255.

* **Solución Final Aplicada:** 
```python
import csv


def limpiar_ip(ip_texto):
    if not ip_texto:
        return None
    
    ip_limpia = ip_texto.strip()
    partes = ip_limpia.split(".")
    
    if len(partes) != 4:
        return None
        
    try:
        for parte in partes:
            numero = int(parte)
            if numero < 0 or numero > 255:
                return None
        return ip_limpia
    except (ValueError, TypeError):
        return None


def limpiar_status(status_texto):
    try:
        numero = int(status_texto)
        if 100 <= numero <= 599:
            return numero
        return None
    except (ValueError, TypeError):
        return None


def cargar_y_deduplicar_logs(ruta_csv):
    registros_validos = []
    registros_vistos = set()

    try:
        with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            
            for fila in lector:
                ip = limpiar_ip(fila.get("ip"))
                status = limpiar_status(fila.get("status"))
                timestamp = fila.get("timestamp")
                endpoint = fila.get("endpoint")

                if not ip or status is None or not timestamp or not endpoint:
                    continue

                clave_unica = (timestamp, ip, endpoint)
                if clave_unica in registros_vistos:
                    continue

                registros_vistos.add(clave_unica)
                metodo = fila.get("metodo", "GET").upper()

                registros_validos.append({
                    "timestamp": timestamp,
                    "ip": ip,
                    "metodo": metodo,
                    "status": status,
                    "endpoint": endpoint
                })

    except FileNotFoundError:
        print("El archivo CSV no fue encontrado.")

    return registros_validos
```


## Registro de Prompt # [3]

* **Fecha:** 2026-10-09

* **Módulo/Función:** src/limpieza.py

* **Prompt Enviado:** "Investigué sobre la librería nativa ipaddress de Python. ¿Es recomendable reemplazar mi función de validación manual por ipaddress.ip_address para simplificar la explicación en la defensa oral?"

* **Respuesta de la IA:** La IA confirmó que utilizar `ipaddress` es una estándar profesional superior, ya que valida automáticamente la estructura IPv4/IPv6 y lanza `ValueError` si los octetos son incorrectos, reduciendo la función a pocas líneas sin necesidad de bucles `for` manuales.

* **Análisis Crítico:** Al evaluar la sugerencia, comprobé que `ipaddress` hace el código más limpio, elegante y fácil de explicar ante el profesor. Decidí refactorizar la función `limpiar_ip` integrando `ipaddress` dentro de un bloque `try/except ValueError`.

* **Solución Final Aplicada:** 
```python
import csv
import ipaddress


def limpiar_ip(ip_texto):
    if not ip_texto:
        return None
    ip_limpia = ip_texto.strip()
    try:
        ipaddress.ip_address(ip_limpia)
        return ip_limpia
    except ValueError:
        return None


def limpiar_status(status_texto):
    try:
        numero = int(status_texto)
        if 100 <= numero <= 599:
            return numero
        return None
    except (ValueError, TypeError):
        return None


def cargar_y_deduplicar_logs(ruta_csv):
    registros_validos = []
    registros_vistos = set()

    try:
        with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            
            for fila in lector:
                ip = limpiar_ip(fila.get("ip"))
                status = limpiar_status(fila.get("status"))
                timestamp = fila.get("timestamp")
                endpoint = fila.get("endpoint")

                if not ip or status is None or not timestamp or not endpoint:
                    continue

                clave_unica = (timestamp, ip, endpoint)
                if clave_unica in registros_vistos:
                    continue

                registros_vistos.add(clave_unica)
                metodo = fila.get("metodo", "GET").upper()

                registros_validos.append({
                    "timestamp": timestamp,
                    "ip": ip,
                    "metodo": metodo,
                    "status": status,
                    "endpoint": endpoint
                })

    except FileNotFoundError:
        print("El archivo CSV no fue encontrado.")

    return registros_validos
```


## Registro de Prompt # [4]

* **Fecha:** 2026-10-09

* **Módulo/Función:** src/limpieza.py

* **Prompt Enviado:** "Tengo una serie de validaciones encadenadas mediante operadores lógicos 'or' para comprobar la presencia e integridad de los 5 campos requeridos en cada fila de mi CSV (IP, Status, Timestamp, Endpoint y Método). ¿Existe alguna función nativa de Python más elegante y pythonica que me permita simplificar esta condición en una sola línea sin perder legibilidad ni rigor en la validación estricta?"

* **Respuesta de la IA:** La IA recomendó utilizar la función nativa `all()` de Python combinada con el operador de negación `not`. Explicó que `all()` evalúa si cada uno de los elementos de una lista es verdadero/válido. Al aplicar `if not all([ip, status, timestamp, endpoint, metodo]):`, la condición ejecuta el `continue` si falta o falla tan solo uno de los campos.

* **Análisis Crítico:** Evalué la propuesta y comprendí el funcionamiento de la evaluación de verdad en Python: `all()` exige la presencia del 100% de los elementos válidos (5 de 5). Si un registro contiene 4 de 5 datos (por ejemplo, le falta el método o la fecha), `all()` retorna `False` y la negación activa el descarte inmediato con `continue`. Esto no solo eliminó las extensas cadenas de `or`, sino que hizo la lógica más limpia, mantenible y fácil de fundamentar técnicamente en la defensa oral del curso.

* **Solución Final Aplicada:** 
```python
import csv
import ipaddress


def limpiar_ip(ip_texto):
    if not ip_texto:
        return None
    
    ip_limpia = ip_texto.strip()
    
    try:
        ipaddress.ip_address(ip_limpia)
        return ip_limpia
    except ValueError:
        return None


def limpiar_status(status_texto):
    try:
        numero = int(status_texto)
        if 100 <= numero <= 599:
            return numero
        return None
    except (ValueError, TypeError):
        return None


def cargar_y_deduplicar_logs(ruta_csv):
    registros_validos = []
    registros_vistos = set()

    try:
        with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            
            for fila in lector:
                ip = limpiar_ip(fila.get("ip"))
                status = limpiar_status(fila.get("status"))
                timestamp = (fila.get("timestamp") or "").strip()
                endpoint = (fila.get("endpoint") or "").strip()
                metodo = (fila.get("metodo") or "").strip().upper()

                if not all([ip, status, timestamp, endpoint, metodo]):
                    continue

                clave_unica = (timestamp, ip, endpoint)
                if clave_unica in registros_vistos:
                    continue

                registros_vistos.add(clave_unica)

                registros_validos.append({
                    "timestamp": timestamp,
                    "ip": ip,
                    "metodo": metodo,
                    "status": status,
                    "endpoint": endpoint
                })

    except FileNotFoundError:
        print("El archivo CSV no fue encontrado.")

    return registros_validos
```


## Registro de Prompt # [5]

* **Fecha:** 2026-10-10

* **Módulo/Función:** src/limpieza_json.py

* **Prompt Enviado:** "Hola, actúa como tutor de Python. Necesito hacer un script para leer data/events.json, pero no quiero que me des todo el código de golpe. Dame las pautas de qué errores o datos feos debo revisar primero para ir haciéndolo yo paso a paso."

* **Respuesta de la IA:** La IA me dio una lista con los 4 fallos principales a cuidar: archivos que no existen, porcentajes de CPU/Memoria negativos o mayores a 100%, datos vacíos y registros duplicados.

* **Análisis Crítico:** Entendí que antes de guardar cualquier evento debía crear una función pequeña `validar_porcentaje()` para controlar que la CPU y Memoria estén entre 0 y 100, y usar `set()` para no guardar eventos repetidos.

* **Solución Final Aplicada:** 
```python
import json

def validar_porcentaje(valor):
    try:
        numero = float(valor)
        if 0.0 <= numero <= 100.0:
            return numero
        return None
    except (ValueError, TypeError):
        return None


def cargar_archivos_json(ruta_json):
    eventos_validos = []
    eventos_vistos = set()

    try:
        with open(ruta_json, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
        for evento in datos:
            event_id = (evento.get("event_id") or "").strip()
            timestamp = (evento.get("timestamp") or "").strip()
            server_id = (evento.get("server_id") or "").strip()

            cpu = validar_porcentaje(evento.get("cpu_percent"))
            memoria = validar_porcentaje(evento.get("memory_percent"))
            status = (evento.get("status") or "").strip().upper()

            if not all([event_id, timestamp, server_id, cpu is not None, memoria is not None, status]):
                continue

            if event_id in eventos_vistos:
                continue
            eventos_vistos.add(event_id)

            eventos_validos.append({
                "event_id": event_id,
                "timestamp": timestamp,
                "server_id": server_id,
                "cpu_percent": cpu,
                "memory_percent": memoria,
                "status": status
            })
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta {ruta_json}")
    except json.JSONDecodeError:
        print(f"Error: El archivo en la ruta {ruta_json} no es un archivo JSON válido")
       
    return eventos_validos
```


## Registro de Prompt # [6]

* **Fecha:** 2026-10-10

* **Módulo/Función:** src/limpieza_json.py

* **Prompt Enviado:** "Hola, revisa mi código de src/limpieza_json.py a ver si está bien o si tiene algún fallo."

* **Respuesta de la IA:** La IA revisó mi código y me dijo que está bien para mi archivo de prueba, pero me advirtió que si en el futuro me dan un archivo gigante (como de 50 GB), cargarlo todo junto a la vez podría llenar la memoria RAM y colapsar la computadora. Me sugirió que si el archivo es grande, es mejor leerlo línea por línea.

* **Análisis Crítico:** Me sirvió mucho esa observación. Aunque mi código funcionaba bien para la tarea actual, entendí el riesgo de llenar la memoria RAM cuando hay muchos datos. Por eso decidí mejorar la función usando `seek(0)` para que pueda leer tanto archivos normales como archivos grandes línea por línea sin congelar la máquina.

* **Solución Final Aplicada:** 
```python
import json


def validar_porcentaje(valor):
    try:
        numero = float(valor)
        if 0.0 <= numero <= 100.0:
            return numero
        return None
    except (ValueError, TypeError):
        return None


def cargar_archivos_json(ruta_json):
    eventos_validos = []
    eventos_vistos = set()

    try:
        with open(ruta_json, mode='r', encoding='utf-8') as archivo:
            try:
                datos = json.load(archivo)
            except json.JSONDecodeError:
                archivo.seek(0)
                datos = []
                for linea in archivo:
                    linea = linea.strip()
                    if not linea:
                        continue
                    try:
                        datos.append(json.loads(linea))
                    except json.JSONDecodeError:
                        continue

            for evento in datos:
                if not isinstance(evento, dict):
                    continue

                event_id = (evento.get("event_id") or "").strip()
                timestamp = (evento.get("timestamp") or "").strip()
                server_id = (evento.get("server_id") or "").strip()

                cpu = validar_porcentaje(evento.get("cpu_percent"))
                memoria = validar_porcentaje(evento.get("memory_percent"))
                status = (evento.get("status") or "").strip().upper()

                if not all([event_id, timestamp, server_id, cpu is not None, memoria is not None, status]):
                    continue

                if event_id in eventos_vistos:
                    continue

                eventos_vistos.add(event_id)

                eventos_validos.append({
                    "event_id": event_id,
                    "timestamp": timestamp,
                    "server_id": server_id,
                    "cpu_percent": cpu,
                    "memory_percent": memoria,
                    "status": status
                })

    except (FileNotFoundError, IOError) as e:
        print(f"Error al abrir el archivo en la ruta {ruta_json}: {e}")

    return eventos_validos
```
