from fastapi import FastAPI, Query
from pydantic import BaseModel
import dns.resolver
import dns.exception

app = FastAPI()


@app.get("/dns-query")
def query_dns(
    domain: str = Query(..., description="Dominio a consultar"),
    rrtype: str = Query("SOA", description="Tipo de registro DNS"),
    nameserver: str = Query(..., description="IP del servidor autoritativo DNS")
):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [nameserver]

    try:
        response = resolver.resolve(domain, rrtype)
        return {
            "domain": domain,
            "type": rrtype,
            "nameserver": nameserver,
            "result": [r.to_text() for r in response]
        }
    except dns.resolver.NXDOMAIN:
        return {"error": f"El dominio {domain} no existe."}
    except dns.resolver.NoAnswer:
        return {"error": f"No hay respuesta para {rrtype} en {domain} desde {nameserver}."}
    except dns.exception.DNSException as e:
        return {"error": f"Error al consultar DNS: {str(e)}"}
