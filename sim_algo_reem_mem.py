#!/usr/bin/env python

def procesar(segmentos, reqs, marcos_libres):
    tabla_paginas = {}
    marcos_ocupados = {}
    cola_fifo = []
    resultados = []

    def obtener_segmento(direccion):
        for nombre, base, limite in segmentos:
            if base <= direccion < base + limite:
                return True
        return False

    for req in reqs:
        if not obtener_segmento(req):
            resultados.append((req, 0x1FF, "Segmention Fault"))
            continue

        pagina = req >> 4
        offset = req & 0xF

        if pagina in tabla_paginas:
            marco = tabla_paginas[pagina]
            resultados.append((req, (marco << 4) | offset, "Marco ya estaba asignado"))
        else:
            if marcos_libres:
                marco = marcos_libres.pop()
                tabla_paginas[pagina] = marco
                cola_fifo.append(pagina)
                resultados.append((req, (marco << 4) | offset, "Marco libre asignado"))
            else:
                pagina_vieja = cola_fifo.pop(0)
                marco = tabla_paginas[pagina_vieja]
                del tabla_paginas[pagina_vieja]
                tabla_paginas[pagina] = marco
                cola_fifo.append(pagina)
                resultados.append((req, (marco << 4) | offset, "Marco asignado"))

    return resultados

def print_results(results):
    for result in results:
        print(f"Req: {result[0]:#04x} Direccion Fisica: {result[1]:#04x} Acción: {result[2]}")

if __name__ == '__main__':
    marcos_libres = [0x0, 0x1, 0x2]
    reqs = [0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1]
    segmentos = [
        ('.text', 0x00, 0x1A),
        ('.data', 0x40, 0x28),
        ('.heap', 0x80, 0x1F),
        ('.stack', 0xC0, 0x22),
    ]
    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)
