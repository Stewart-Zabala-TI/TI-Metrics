import json
from src.limpieza_csv import cargar_y_deduplicar_logs
from src.limpieza_json import cargar_archivos_json
from src.cliente_api import consultar_api


def generar_reporte():
    logs = cargar_y_deduplicar_logs("data/logs.csv")
    eventos = cargar_archivos_json("data/events.json")

    total_logs = len(logs)
    errores_500 = 0
    ips_criticas_vistas = set()
    ips_criticas_enriquecidas = []

    for log in logs:
        if log.get("status") == 500:
            errores_500 += 1
            ip = log.get("ip")
            if ip and ip not in ips_criticas_vistas:
                ips_criticas_vistas.add(ip)
                geo_info = consultar_api(ip)
                ips_criticas_enriquecidas.append({
                    "ip": ip,
                    "endpoint": log.get("endpoint"),
                    "geolocalizacion": geo_info
                })

    try:
        porcentaje_500 = (errores_500 / total_logs) * 100
    except ZeroDivisionError:
        porcentaje_500 = 0.0

    reporte = {
        "metricas_logs": {
            "total_logs_procesados": total_logs,
            "cantidad_errores_500": errores_500,
            "porcentaje_errores_500": round(porcentaje_500, 2)
        },
        "ips_criticas": ips_criticas_enriquecidas,
        "resumen_infraestructura": {
            "total_eventos_procesados": len(eventos)
        }
    }

    try:
        with open("data/reporte_resumen.json", mode="w", encoding="utf-8") as archivo:
            json.dump(reporte, archivo, indent=4)
        print("Reporte generado exitosamente en data/reporte_resumen.json")
    except IOError as e:
        print(f"Error al escribir el reporte: {e}")


if __name__ == "__main__":
    generar_reporte()
