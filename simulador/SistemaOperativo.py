from Memoria import Memoria
from Particion import Particion
from Proceso import Proceso
from Cola import Cola

class SistemaOperativo:
  
  def __init__(self):
    self.tiempo: int = 0
    self.arribos: list[str] = []
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
  
  def cargarArchivo(ruta: str) -> None:
    pass
  
  def cargarNuevos() -> None:
    pass
  
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