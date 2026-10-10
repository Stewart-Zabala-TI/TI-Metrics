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
