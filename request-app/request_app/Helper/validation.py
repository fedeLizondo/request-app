import ipaddress

# Definimos las redes locales y especiales
local_networks = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
    ipaddress.IPv4Network("127.0.0.0/8"),   # Loopback
    ipaddress.IPv4Network("169.254.0.0/16") # APIPA
]

# Red link-local IPv6
link_local_ipv6 = ipaddress.IPv6Network("fe80::/10")

def is_local_ip(ip: str) -> bool:
    try:
        # Convertimos la IP a un objeto de tipo IP
        ip_obj = ipaddress.ip_address(ip)
        
        # Verificamos si la IP es IPv4 y si está dentro de alguna de las redes locales
        if isinstance(ip_obj, ipaddress.IPv4Address):
            return any(ip_obj in network for network in local_networks)
        
        # Verificamos si la IP es IPv6 y si está en la red link-local IPv6
        elif isinstance(ip_obj, ipaddress.IPv6Address):
            return ip_obj in link_local_ipv6
        
    except ValueError:
        # Si la IP es inválida
        return False