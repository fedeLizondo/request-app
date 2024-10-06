import re
from Entity.ParserInterface import ParserInterface
from Helper.validation import is_local_ip
from urllib.parse import urlparse, parse_qs


class ParserTcpDump(ParserInterface):
    def parse_data(self, data: str) -> dict:
        # Expresiones regulares para capturar la IP, puertos, fecha/hora, request/respuesta HTTP, etc.
        ip_regex = r"IP (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}).(\d+) . (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}).(\d+)"
        request_regex = r"(GET|POST) (.+?) HTTP"
        # Para capturar respuestas HTTP
        response_regex = r"HTTP/1.1 (\d{3}) (.+)"
        user_agent_regex = r"User-Agent: (.+)"
        content_type_regex = r"Content-Type: (.+)"
        content_length_regex = r"Content-Length: (\d+)"
        # Captura la hora con milisegundos
        timestamp_regex = r"(\d{2}:\d{2}:\d{2}\.\d+)"

        # Buscar la fecha y hora en la cadena
        timestamp_match = re.search(timestamp_regex, data)
        if timestamp_match:
            timestamp = timestamp_match.group(1)
        else:
            timestamp = None

        # Buscar las IPs y puertos en la cadena
        ip_match = re.search(ip_regex, data)
        if ip_match:
            ip_origen = ip_match.group(1)
            port_origen = ip_match.group(2)
            ip_destino = ip_match.group(3)
            port_destino = ip_match.group(4)
        else:
            ip_origen, port_origen, ip_destino, port_destino = None, None, None, None

        # Buscar el request en la cadena (GET/POST)
        request_match = re.search(request_regex, data)
        if request_match:
            action_type = request_match.group(1)
            request_path = request_match.group(2)
        else:
            action_type, request_path = None, None

        # Buscar el response en la cadena (HTTP response)
        response_match = re.search(response_regex, data)
        if response_match:
            response_code = response_match.group(1)
            response_message = response_match.group(2)
        else:
            response_code, response_message = None, None

        # Buscar el User-Agent en la cadena
        user_agent_match = re.search(user_agent_regex, data)
        user_agent = user_agent_match.group(1) if user_agent_match else None

        # Buscar el Content-Type en la cadena
        content_type_match = re.search(content_type_regex, data)
        content_type = content_type_match.group(
            1) if content_type_match else None

        # Buscar el Content-Length en la cadena
        content_length_match = re.search(content_length_regex, data)
        content_length = content_length_match.group(
            1) if content_length_match else None

        # Verificar si la IP de origen es local
        is_local = is_local_ip(ip_origen)

        # Create Variable to validate
        variables = {}

        if (request_path != None):
            parsed_url = urlparse(request_path)
            query_params = parse_qs(parsed_url.query)
            query_params_simple = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
            variables["query"] = query_params_simple


        # Retornar la información en formato de diccionario
        return {
            "timestamp": timestamp,
            "ip_origen": ip_origen,
            "port_origen": port_origen,
            "ip_destino": ip_destino,
            "port_destino": port_destino,
            "action_type": action_type,  # Si es request (GET/POST)
            "request_path": request_path,
            "response_code": response_code,  # Si es response
            "response_message": response_message,
            "user_agent": user_agent,
            "content_type": content_type,
            "content_length": content_length,
            "is_local": is_local,
            'validata': variables
        }
