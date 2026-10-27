
class Proceso:
  genId: int = 0
  
  def __init__(self,tArribo: int,tIrrupcion: int,tamaño: int,id: int = None) -> None:
    self.id = id if id else self.siguienteId()
    self.tArribo = tArribo
    self.tIrrupcion = tIrrupcion
    self.tamaño = tamaño
    self.tEjecutando: int = 0
    self.tTerminado: int = None
  
  def siguienteId(self) -> int:
    Proceso.genId += 1
    return Proceso.genId
  
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