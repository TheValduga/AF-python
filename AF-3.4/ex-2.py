from time import sleep
from random import randint
from threading import Thread, Semaphore

def produtor():
  global buffer
  for i in range(10):
    sleep(randint(0,2))           # fica um tempo produzindo...
    item = 'item ' + str(i)
    sem_lugares.acquire() # verifica se há lugar no buffer
    buffer.append(item)
    print('Produzido %s (ha %i itens no buffer)' % (item,len(buffer)))
    sem_itens.release()

def consumidor():
  global buffer
  for i in range(10):
    sem_itens.acquire() # aguarda que haja um item para consumir
    item = buffer.pop(0)
    print('Consumido %s (ha %i itens no buffer)' % (item,len(buffer)))
    sleep(randint(0,2))         # fica um tempo consumindo...
    sem_lugares.release()

buffer = []
tam_buffer = 3
# cria semáforos
sem_itens = Semaphore(0)
sem_lugares = Semaphore(tam_buffer)
produtor = Thread(target=produtor) 
consumidor = Thread(target=consumidor) 
produtor.start()
consumidor.start()
produtor.join()
consumidor.join() 