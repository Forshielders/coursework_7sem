# coursework_7sem

Для работы необходимо скчать этот проект на локальное устройство, импортировать нужные функции и запустить симуляцию

Пример: 

```python
from coursework_7sem import start_simulation
from coursework_7sem import set_config

set_config({
    "CLIENT_WAIT_TIME": 1,
    "PROXMPX_CLASTER_CPU": 150
})

start_simulation(clients=3, until=100)
```

set_config поменяет указаные параметры, а start_simulation запустит симуляцию с указанным кол-вом клиентов и временем работы.

После запуска появится json файл с результатами симуляции.