import requests

def consultar_api(ip_texto):

    if not ip_texto:
        return None
    
    ip_limpia= ip_texto.strip()
    url=f"http://ip-api.com/json/{ip_limpia}"

    try:
        response = requests.get(url,timeout = 5)
        response.raise_for_status()

        datos = response.json()

        if datos.get("status") == "success":
            return datos
        
        return None
    except requests.exceptions.Timeout:
        print(f"Error: La consulta para la IP {ip_limpia} tardó demasiado en responder.")
        return None
    except requests.exceptions.RequestException as error:
        print(f"Error HTTP o de Red al consulta la ip: {ip_limpia}: {error }")
        return None