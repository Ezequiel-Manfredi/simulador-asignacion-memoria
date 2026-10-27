from typing import Callable
from Proceso import Proceso

class Cola:
  def __init__(self, orden: Callable[[Proceso,Proceso],bool] = None) -> None:
    self.procesos: list[Proceso] = []
    self.orden = orden
  
  def agregar(self,proceso: Proceso) -> None:
    if self.orden != None and len(self.procesos) >= 1:
      for i,p in enumerate(self.procesos):
        if self.orden(proceso,p):
          self.procesos.insert(i,proceso)
          break
      else:
        self.procesos.append(proceso)
    else:
      self.procesos.append(proceso)
  
  def siguiente(self) -> Proceso:
    return self.procesos[0]
  
  def eliminar(self, proceso: Proceso) -> Proceso:
    indice = self.procesos.index(proceso)
    return self.procesos.pop(indice)
  
  def __str__(self) -> str:
    txt = "id\ttr\n"
    for p in self.procesos:
      txt = txt + p.__str__()
    return txt

if __name__ == "__main__":
  cola = Cola(lambda x,y : x.tRestante() < y.tRestante())
  p1 = Proceso(0,1,50)
  p2 = Proceso(0,1,100)
  p3 = Proceso(0,2,150)

  cola.agregar(p3)
  cola.agregar(p2)
  cola.agregar(p1)
  print(cola)
