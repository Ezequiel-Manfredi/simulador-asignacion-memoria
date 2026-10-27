
class Proceso:
  genId: int = 1
  
  def __init__(self,tArribo: int,tIrrupcion: int,tamaño: int) -> None:
    self.id = Proceso.genId
    Proceso.genId += 1
    self.tArribo = tArribo
    self.tIrrupcion = tIrrupcion
    self.tamaño = tamaño
    self.tEjecutando: int = 0
    self.tTerminado: int = None
  
  def ejecutar(self, tProcesador: int) -> None:
    if self.aTerminado():
      return
    self.tEjecutando += 1
    if self.aTerminado():
      self.tTerminado = tProcesador
  
  def tRestante(self) -> int:
    return self.tIrrupcion - self.tEjecutando
  
  def aTerminado(self) -> bool:
    return self.tRestante() == 0

  def __str__(self) -> str:
    return f"{self.id}\t{self.tRestante()}\n"