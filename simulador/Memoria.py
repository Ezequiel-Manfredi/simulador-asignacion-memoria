from Particion import Particion, TipoParticion
from Proceso import Proceso

class Memoria:
  
  def __init__(self,tamaño: int, mp: bool = False) -> None:
    baseUsu = 0
    self.particiones: list[Particion] = []
    self.tamaño = tamaño
    if mp and tamaño > 100:
      so = Particion(TipoParticion.SO,0,100)
      self.particiones.append(so)
      tamaño -= 100
      baseUsu = 100
    usu = Particion(TipoParticion.HUECO,baseUsu,tamaño)
    self.particiones.append(usu)
  
  def guardar(self,proceso: Proceso) -> bool:
    particion: Particion = None
    for p in self.particiones:
      if p.estaAsignada() or proceso.tamaño > p.tamaño:
        continue
      if p.esMenor(particion):
        particion = p
    if particion:
      if particion > proceso.tamaño:
        tSobra = particion.tamaño - proceso.tamaño
        sobra = Particion(TipoParticion.HUECO,proceso.tamaño,tSobra)
        self.particiones.insert(self.particiones.index(particion)+1,sobra)
      particion.setProceso(proceso)
      return True 
    return False
  
  def liberar(self,proceso: Proceso) -> Particion:
    for p in self.particiones:
      if p.tipo == TipoParticion.PROCESO and p.proceso.id == proceso.id:
        p.limpiar()
        return p
