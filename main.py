import heapq
import time


class GrafoVuelos:
    def __init__(self):
        self.adyacencia = {}

    def cargar_datos(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                for linea in f:
                    linea = linea.strip()
                    if linea:
                        origen, dest, precio, aerolinea = linea.split(',')
                        self.agregar_vuelo(
                            origen.strip().upper(),
                            dest.strip().upper(),
                            float(precio.strip()),
                            aerolinea.strip()
                        )
            print(f"-> Base de datos '{ruta_archivo}' cargada correctamente.")
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{ruta_archivo}'.")

    def agregar_vuelo(self, u, v, peso, aerolinea):
        if u not in self.adyacencia:
            self.adyacencia[u] = []
        if v not in self.adyacencia:
            self.adyacencia[v] = []
        self.adyacencia[u].append((v, peso, aerolinea))

    def reporteria(self):
        print("\n" + "=" * 45)
        print("       REPORTE DE CONEXIONES REGISTRADAS")
        print("=" * 45)
        for nodo, rutas in self.adyacencia.items():
            print(f"\nAeropuerto [{nodo}]: {len(rutas)} vuelos de salida")
            for destino, precio, aerolinea in rutas:
                print(f"   └──> Hacia {destino} | Tarifa: ${precio:.2f} ({aerolinea})")
        print("=" * 45 + "\n")

    def dijkstra_vuelo_barato(self, inicio, meta):
        cola = [(0.0, inicio, [])]
        visitados = set()

        while cola:
            costo, actual, ruta = heapq.heappop(cola)

            if actual in visitados:
                continue
            visitados.add(actual)

            ruta = ruta + [actual]

            if actual == meta:
                return costo, ruta

            for vecino, precio, _ in self.adyacencia.get(actual, []):
                if vecino not in visitados:
                    heapq.heappush(cola, (costo + precio, vecino, ruta))

        return float('inf'), []


if __name__ == "__main__":
    sistema = GrafoVuelos()

    # Cargar datos
    sistema.cargar_datos("vuelos.txt")

    # Reportería de conexiones
    sistema.reporteria()

    # Búsqueda
    print("--- BÚSQUEDA DE RUTA MÁS ECONÓMICA ---")
    origen = input("Ingrese código del aeropuerto origen (ej. UIO): ").upper()
    destino = input("Ingrese código del aeropuerto destino (ej. MIA): ").upper()

    inicio_tiempo = time.perf_counter()
    costo_total, ruta_optima = sistema.dijkstra_vuelo_barato(origen, destino)
    fin_tiempo = time.perf_counter()

    tiempo_ms = (fin_tiempo - inicio_tiempo) * 1000

    print("\n" + "-" * 40)
    if costo_total != float('inf'):
        print(f"Ruta más económica: {' -> '.join(ruta_optima)}")
        print(f"Costo total del vuelo: ${costo_total:.2f} USD")
        print(f"Número de escalas: {len(ruta_optima) - 2}")
    else:
        print(f"No existe ninguna ruta disponible entre {origen} y {destino}.")

    print(f"Tiempo de ejecución del algoritmo: {tiempo_ms:.4f} ms")
    print("-" * 40)