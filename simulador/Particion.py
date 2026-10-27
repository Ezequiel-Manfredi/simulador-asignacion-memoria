from enum import Enum
from typing import Self
from Proceso import Proceso

class TipoParticion(Enum):
  SO = 1
  HUECO = 2
  PROCESO = 3

class Particion:
  genId = 1
  
  def __init__(self,tipo: TipoParticion,base: int,tamaño: int) -> None:
    self.setId()
    self.tipo = tipo if tipo != TipoParticion.PROCESO else TipoParticion.HUECO
    self.base = base
    self.tamaño = tamaño
    self.proceso: Proceso = None
  
  def setId(self) -> None:
    self.id = Particion.genId
    Particion.genId += 1
  
  def setProceso(self,proceso: Proceso) -> None:
    if self.tipo == TipoParticion.HUECO:
      self.setId()
      self.proceso = proceso
      self.tipo = TipoParticion.PROCESO
      self.tamaño = proceso.tamaño
  
  def estaAsignada(self) -> bool:
    return self.tipo != TipoParticion.HUECO
  
  def esMenor(self,p: Self | None) -> bool:
    return True if not p else (self.tamaño < p.tamaño)
  
  def limpiar(self) -> None:
    self.setId()
    self.tipo = TipoParticion.HUECO
    self.proceso = None
    
if __name__=="__main__":
  p = Particion(TipoParticion.SO,0,100)
  print(p.esMenor(p))
