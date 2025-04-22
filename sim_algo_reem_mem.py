#!/usr/bin/env python

marcos_libres = [0x0, 0x1, 0x2]
reqs = [0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A]
segmentos = [
    ('.text', 0x00, 0x1A),
    ('.data', 0x40, 0x28),
    ('.heap', 0x80, 0x1F),
    ('.stack', 0xC0, 0x22),
]

def procesar(segmentos, reqs, marcos_libres):
    tabla_segmentos = []
    for nombre, base, limite in segmentos:
        for i in range(base, base + limite):
            tabla_segmentos.append(i)

    tabla_paginas = {}  # página → marco
    cola_fifo = []      # páginas en orden de carga FIFO
    resultados = []

    for req in reqs:
        if req not in tabla_segmentos:
            resultados.append((req, 0x1FF, "Segmention Fault"))
            continue

        pagina = req >> 4
        offset = req & 0xF

        if pagina in tabla_paginas:
            marco = tabla_paginas[pagina]
            direccion_fisica = (marco << 4) | offset
            resultados.append((req, direccion_fisica, "Marco ya estaba asignado"))
        else:
            if marcos_libres:
                marco = marcos_libres.pop(0)
                tabla_paginas[pagina] = marco
                cola_fifo.append(pagina)
                direccion_fisica = (marco << 4) | offset
                resultados.append((req, direccion_fisica, "Marco libre asignado"))
            else:
                pagina_a_remover = cola_fifo.pop(0)
                marco = tabla_paginas.pop(pagina_a_remover)
                tabla_paginas[pagina] = marco
                cola_fifo.append(pagina)
                direccion_fisica = (marco << 4) | offset
                resultados.append((req, direccion_fisica, "Marco asignado"))

    return resultados

def print_results(results):
    for result in results:
        print(f"Req: {result[0]:#0{4}x} Direccion Fisica: {result[1]:#0{4}x} Acción: {result[2]}")

if __name__ == '__main__':
    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)
