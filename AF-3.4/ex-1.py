from time import sleep
from random import randint
from threading import Thread, Lock, Condition, current_thread

def produtor():
  global buffer
  for i in range(10):
    sleep(randint(0,2))           # fica um tempo produzindo...
    if current_thread().name == "P1":
      item = 'item ' + str(i)
    else:
      item = 'item ' + str(i+10)
    with lock_prod:
      with lock:
        if len(buffer) == tam_buffer:
          print(f'>>> Buffer cheio. Produtor {current_thread().name} ira aguardar.')
          lugar_no_buffer.wait()    # aguarda que haja lugar no buffer
        buffer.append(item)
        print(f'{current_thread().name}: Produzido {item} (ha {len(buffer)} itens no buffer)')
        item_no_buffer.notify()

def consumidor():
  global buffer
  for i in range(10):
    with lock_cons:
      with lock:
        if len(buffer) == 0:
          print(f'>>> Buffer vazio. Consumidor {current_thread().name} ira aguardar.')
          item_no_buffer.wait()   # aguarda que haja um item para consumir 
        item = buffer.pop(0)
        print(f'{current_thread().name}: Consumido {item} (ha {len(buffer)} itens no buffer)')
        lugar_no_buffer.notify()
      sleep(randint(0,2))         # fica um tempo consumindo...

buffer = []
tam_buffer = 5
lock = Lock()
lock_prod = Lock()
lock_cons = Lock()
lugar_no_buffer = Condition(lock)
item_no_buffer = Condition(lock)
produtor1 = Thread(target=produtor,name="P1") 
produtor2 = Thread(target=produtor,name="P2") 
consumidor1 = Thread(target=consumidor,name="C1") 
consumidor2 = Thread(target=consumidor,name="C2") 
produtor1.start()
consumidor1.start()
produtor2.start()
consumidor2.start()
produtor1.join()
consumidor1.join()
produtor2.join()
consumidor2.join()