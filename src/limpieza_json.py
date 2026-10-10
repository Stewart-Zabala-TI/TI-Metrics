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