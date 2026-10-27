import re
from Memoria import Memoria
from Particion import Particion
from Proceso import Proceso
from Cola import Cola

class SistemaOperativo:
  
  def __init__(self):
    self.tiempo: int = 0
    self.arribos: list[dict[str,int]] = []
    self.eventos: list[str] = []
    self.hayEventos: bool = False
    self.ejecutando: Proceso = None
    self.nuevos: Cola = Cola(lambda x,y : x.tArribo < y.tArribo)
    self.listos: Cola = Cola(lambda x,y : x.tRestante() < y.tRestante())
    self.listosySusp: Cola = Cola(lambda x,y : x.tRestante() < y.tRestante())
    self.terminados: Cola = Cola()
    self.memoriaPrincipal: Memoria = Memoria(550,True)
    self.memoriaAuxiliar: Memoria = Memoria(1000)

  def registrarEvento(self,evento: str) -> None:
    self.eventos.append(evento)
  
  def cargarArchivo(self) -> None:
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
          if len(self.arribos) >= 10:
            print("\tError: no se permiten más de 10 procesos.")
            archivo.close()
            archivo = None
            self.arribos.clear()
            break
          info = re.match("\\d+,\\d+,\\d+,\\d+",linea)
          if not info:
            print("\tError: archivo sin formato correcto (ej. 1,2,3,4)")
            archivo.close()
            archivo = None
            self.arribos.clear()
            break
          
          informacion = linea.strip().split(",")
          self.arribos.append({
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
    self.arribos.sort(key=lambda x: x["ta"])
    print("- Archivo cargado correctamente.")
  
  def cargarNuevos(self) -> None:
    while len(self.arribos) > 0 and self.arribos[0]["ta"] == self.tiempo:
      proceso = self.arribos.pop(0)
      self.nuevos.agregar(Proceso(proceso['ta'],proceso['ti'],proceso['tam'],proceso['id']))
      self.registrarEvento(f"Proceso {proceso['id']} ha llegado a la cola de nuevos.")
  
  def admitirProcesos() -> None:
    pass
  
  def reasignarParticion(particion: Particion) -> None:
    pass
  
  def generarInforme() -> None:
    pass
  
  def ciclo() -> None:
    pass

if __name__ == "__main__":
  so = SistemaOperativo()