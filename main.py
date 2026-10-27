import re

pausar = True
colaArribo = []
colaNuevo = []
colaListo = []
colaListoySuspendido = []
colaTerminado = []
memoriaPrincipal = [
  {"id": 0,"idp": -1,"tipo": "so","base": 0, "tamaño": 100},
  {"id": 1,"idp": -1,"tipo": "hueco","base": 100, "tamaño": 450}
]
idPrincipal = 2
memoriaAuxiliar = []
idAuxiliar = 0
procesoEjecutando = None
tiempo = 0
ocurrioEvento = False
eventos = []

def imprimirColasyMemoria():
  print("\nEstado de CPU: ", end='')
  if procesoEjecutando:
    print("Ejecutando un proceso")
    print("ID\tTA\tTI\tTAM\tTX\tTO")
    print(f"{procesoEjecutando['id']}\t{procesoEjecutando['ta']}\t{procesoEjecutando['ti']}", end='')
    print(f"\t{procesoEjecutando['tam']}\t{procesoEjecutando.get('tx','-')}\t{procesoEjecutando.get('to','-')}")
  else:
    print("Libre.")

  memorias = [
    {"msj": "\nMemoria principal:", "memoria": memoriaPrincipal},
    {"msj": "\nMemoria auxiliar:", "memoria": memoriaAuxiliar}
  ]
  for m in memorias:
    print(m["msj"])
    print("ID\tIDP\tTIPO\tBASE\tLÍMITE")
    for particion in m["memoria"]:
      print(f"{particion['id']}\t{particion['idp']}\t{particion['tipo']}\t{particion['base']}\t{particion['limite']}")

  colas = [
    {"msj": "\nCola de arribo:", "cola": colaArribo},
    {"msj": "\nCola de nuevos:", "cola": colaNuevo},
    {"msj": "\nCola de listos:", "cola": colaListo},
    {"msj": "\nCola de listos y suspendidos:", "cola": colaListoySuspendido},
    {"msj": "\nCola de terminados:", "cola": colaTerminado}
  ]
  for c in colas:
    print(c["msj"])
    print("ID\tTA\tTI\tTAM\tTX\tTO")
    for proceso in c["cola"]:
      print(f"{proceso['id']}\t{proceso['ta']}\t{proceso['ti']}\t{proceso['tam']}\t{proceso.get('tx','-')}\t{proceso.get('to','-')}")

def registrarEvento(evento):
  global ocurrioEvento
  ocurrioEvento = True
  eventos.append(f"- {evento}")

def imprimirEventos():
  global ocurrioEvento
  print("\n=====================================")
  print(f"\nTiempo: {tiempo}")
  print("\nEventos:")
  for evento in eventos:
    print(evento)
  eventos.clear()
  input("\nPresione Enter para ver estado de memoria y colas...")
  imprimirColasyMemoria()
  input("\nPresione Enter para ir al siguiente ciclo con eventos...")
  ocurrioEvento = False

def cargarArchivo():
  archivo = None
  
  print("\nIngrese la ruta al archivo de entrada a simular")
  while not archivo:
    ruta = input("- Ruta relativa o absoluta: ")
    try:
      archivo = open(ruta, "r")
      encabezado = re.match('id,ta,ti,tam', archivo.readline())
      if not encabezado:
        print("\tError: archivo sin encabezado correcto (id,ta,ti,tam)")
        archivo.close()
        archivo = None
        continue
      print("- Cargando archivo de entrada...")
      for linea in archivo:
        if len(colaArribo) >= 10:
          print("\tError: no se permiten más de 10 procesos.")
          archivo.close()
          archivo = None
          colaArribo.clear()
          break
        info = re.match("\\d+,\\d+,\\d+,\\d+",linea)
        if not info:
          print("\tError: archivo sin formato correcto (ej. 1,2,3,4)")
          archivo.close()
          archivo = None
          colaArribo.clear()
          break
        
        informacion = linea.strip().split(",")
        colaArribo.append({
          "id": int(informacion[0]), 
          "ta": int(informacion[1]), 
          "ti": int(informacion[2]), 
          "tam": int(informacion[3])
        })
    except FileNotFoundError:
        print("\tError: No se encontró el archivo de entrada.")
        archivo = None
    finally:
      if archivo:
        archivo.close()
  colaArribo.sort(key=lambda x: x["ta"])
  print("- Archivo cargado correctamente.")

def cargarProcesosNuevos():
  while len(colaArribo) > 0 and colaArribo[0]["ta"] == tiempo:
    proceso = colaArribo.pop(0)
    proceso["tx"] = 0
    colaNuevo.append(proceso)
    registrarEvento(f"Proceso {proceso['id']} ha llegado a la cola de nuevos.")

def buscarMejorHueco(tamaño):
  mejorHueco = None

  for particion in memoriaPrincipal:
    if particion["tipo"] == "hueco" and particion["tamaño"] >= tamaño:
      if mejorHueco is None or particion["tamaño"] < mejorHueco["tamaño"]:
        mejorHueco = particion

  return mejorHueco

def cargarEnMemoria(proceso):
  global memoriaPrincipal, idPrincipal, idAuxiliar
  pcb = {
    "id": None,
    "idp": proceso["id"],
    "tipo": "proceso",
    "base": None,
    "tamaño": proceso["tam"]
  }
  particion = buscarMejorHueco(proceso["tam"])
  
  if particion is not None:
    pcb["id"] = idPrincipal
    pcb["base"] = particion["base"]
    idPrincipal += 1
    indice = memoriaPrincipal.index(particion)

    if particion["tamaño"] > proceso["tam"]:
      hueco = {
        "id": idPrincipal,
        "idp": -1,
        "tipo": "hueco",
        "base": particion["base"] + proceso["tam"],
        "tamaño": particion["tamaño"] - proceso["tam"]
      }
      idPrincipal += 1
      memoriaPrincipal.insert(indice + 1, hueco)

    memoriaPrincipal[indice] = pcb
    registrarEvento(f"Proceso {proceso['id']} ha sido cargado en memoria principal.")
    return colaListo

  registrarEvento(f"No hay suficiente memoria principal para admitir el proceso {proceso['id']}.")

  nuevaBase = memoriaAuxiliar[-1]["base"] + memoriaAuxiliar[-1]["tamaño"] if memoriaAuxiliar else 0
  pcb["id"] = idAuxiliar
  pcb["base"] = nuevaBase
  idAuxiliar += 1
  memoriaAuxiliar.append(pcb)
  registrarEvento(f"Proceso {proceso['id']} ha sido cargado en memoria auxiliar.")
  return colaListoySuspendido

def tiempoRestante(proceso):
  return proceso["ti"] - proceso["tx"]

def ordenarProcesoEnCola(cola, proceso):
  for i,p in enumerate(cola):
    if tiempoRestante(p) > tiempoRestante(proceso):
      cola.insert(i, proceso)
      break
  else:
    cola.append(proceso)

def admitirProcesos():
  cantidadProcesos = lambda : len(colaListo) + len(colaListoySuspendido) + (1 if procesoEjecutando else 0)
  while len(colaNuevo) > 0 and cantidadProcesos() < 5:
    proceso = colaNuevo.pop(0)
    cola = cargarEnMemoria(proceso)
    ordenarProcesoEnCola(cola, proceso)
    registrarEvento(f"Proceso {proceso['id']} ha sido admitido.")

def liberarMemoria(proceso, memoria):
  for i,particion in enumerate(memoria):
    if particion["idp"] == proceso["id"]:
      # mirar procesos adyacentes para fusionar huecos
      if i < len(memoria) - 1 and memoria[i + 1]["tipo"] == "hueco":
        particion["tamaño"] += memoria[i + 1]["tamaño"]
        memoria.pop(i + 1)
      if i > 0 and memoria[i - 1]["tipo"] == "hueco":
        particion["base"] = memoria[i - 1]["base"]
        particion["tamaño"] += memoria[i - 1]["tamaño"]
        memoria.pop(i - 1)
      particion["idp"] = -1
      particion["tipo"] = "hueco"
      registrarEvento(f"Proceso {proceso['id']} ha sido liberado de memoria.")
      return particion

def reasignarMemoriaPrincipal(particion):
  global idPrincipal
  # REFLEJAR ESTO EN EL DIAGRAMA DE FLUJO: ni bien liberado memoria se comprueba que algun suspendido pueda entrar
  for proceso in colaListoySuspendido:
    if particion["tamaño"] < proceso["tam"]:
      continue
    if particion["tamaño"] > proceso["tam"]:
      hueco = {
        "id": idPrincipal,
        "idp": -1,
        "tipo": "hueco",
        "base": particion["base"] + proceso["tam"],
        "tamaño": particion["tamaño"] - proceso["tam"]
      }
      idPrincipal += 1
      memoriaPrincipal.insert(memoriaPrincipal.index(particion) + 1, hueco)
    particion["idp"] = proceso["id"]
    particion["tipo"] = "proceso"
    particion["tamaño"] = proceso["tam"]
    liberarMemoria(proceso, memoriaAuxiliar)
    registrarEvento(f"Proceso {proceso['id']} paso de la memoria auxiliar a la memoria principal.")
    ordenarProcesoEnCola(colaListo, colaListoySuspendido.pop(colaListoySuspendido.index(proceso)))
    registrarEvento(f"Proceso {proceso['id']} paso de la cola de Listo y Suspendido a la cola de Listo.")
    break

def ejecutarProceso():
  global procesoEjecutando
  hayProcesosListos = lambda : len(colaListo) > 0
  
  if hayProcesosListos():
    if procesoEjecutando == None:
      procesoEjecutando = colaListo.pop(0)
      registrarEvento(f"Proceso {procesoEjecutando['id']} ha comenzado a ejecutarse.")
      return
    else:
      if tiempoRestante(procesoEjecutando) > tiempoRestante(colaListo[0]):
        registrarEvento(f"Proceso {procesoEjecutando['id']} ha sido interrumpido por el proceso {colaListo[0]['id']}.")
        ordenarProcesoEnCola(colaListo, procesoEjecutando)
        procesoEjecutando = colaListo.pop(0)
        registrarEvento(f"Proceso {procesoEjecutando['id']} ha comenzado a ejecutarse.")
        return
        
  if procesoEjecutando != None:
    procesoEjecutando["tx"] += 1
    if procesoEjecutando["ti"] == procesoEjecutando["tx"]:
      procesoEjecutando["to"] = tiempo
      registrarEvento(f"Proceso {procesoEjecutando['id']} ha terminado su ejecución.")
      colaTerminado.append(procesoEjecutando)
      particion = liberarMemoria(procesoEjecutando, memoriaPrincipal)
      reasignarMemoriaPrincipal(particion)
      if hayProcesosListos():
        procesoEjecutando = colaListo.pop(0)
        registrarEvento(f"Proceso {procesoEjecutando['id']} ha comenzado a ejecutarse.")
      else:
        procesoEjecutando = None

def generarInformeEstadistico():
  sumatoriaTiempoRetorno = 0
  sumatoriaTiempoEspera = 0
  cantidadProcesosSimulados = 0
  
  print("\n=====================================")
  print("\n         INFORME ESTADISTICO")
  print("\nTiempos de Retorno y Espera por cada proceso")
  print("ID\tTR\tTE")
  
  for proceso in colaTerminado:
    tiempoRetorno = proceso["to"] - proceso["ta"]
    tiempoEspera = tiempoRetorno - proceso["ti"]
    print(f"{proceso['id']}\t{tiempoRetorno}\t{tiempoEspera}")
    sumatoriaTiempoRetorno += tiempoRetorno
    sumatoriaTiempoEspera += tiempoEspera
    cantidadProcesosSimulados += 1
  print(f"total\t{sumatoriaTiempoRetorno}\t{sumatoriaTiempoEspera}")
  print(f"\nCantidad de procesos simulados: {cantidadProcesosSimulados}")
  print(f"\nPromedio de Tiempo de Retorno: {(sumatoriaTiempoRetorno/cantidadProcesosSimulados):.2f}")
  print(f"\nPromedio de Tiempo de Espera: {(sumatoriaTiempoEspera/cantidadProcesosSimulados):.2f}")
  print(f"\nEl Rendimiento del Sistema es de {(cantidadProcesosSimulados/tiempo):.2f} cantidad de trabajo por unidad de tiempo.\n")

def bucle():
  global tiempo
  cantidadProcesos = lambda : len(colaArribo) + len(colaNuevo) + len(colaListo) + len(colaListoySuspendido)
  quedanProcesos = lambda : cantidadProcesos() > 0 or procesoEjecutando != None
  
  while quedanProcesos():
    cargarProcesosNuevos()
    admitirProcesos()
    ejecutarProceso()
    
    if ocurrioEvento and pausar:
      imprimirEventos()
    tiempo += 1

  generarInformeEstadistico()

if __name__ == "__main__":
  print("\nSimulador de planificación de procesos")
  print("\n=====================================")
  cargarArchivo()
  print("Iniciando simulación...")
  bucle()
