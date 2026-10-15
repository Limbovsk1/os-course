
# ПР-3. Процессы в Linux (вариант B)

## Цель
Наблюдать процессы средствами ОС, научиться создавать, ожидать и завершать их программно.

## Задание 1. ptree.py — дерево процессов по /proc

```
python3 ptree.py
```

Программа читает /proc/<pid>/status (PPid, State, VmRSS, Uid) и /proc/<pid>/comm
без ps, фильтрует по текущему uid и строит дерево с отступами. Корни дерева —
процессы, чей PPID не указывает на процесс этого же пользователя.

Для сравнения — штатный взгляд ОС на то же самое:

```
ps -eo pid,ppid,stat,cmd --forest | head -40
```

PID 1 в системе — init (в WSL2 — /init), самый первый процесс, предок всех.
Мой bash виден в дереве как ребёнок терминала (wslhost/ Relay).

## Задание 2. runner.py — N процессов с exec

```
python3 runner.py 4 sleep 1
```

Вывод:

```
total wall time: 1.0XXs
child 0: pid=XXXX exit=0 time=1.00Xs
child 1: pid=XXXX exit=0 time=1.00Xs
child 2: pid=XXXX exit=0 time=1.00Xs
child 3: pid=XXXX exit=0 time=1.00Xs
```

```
python3 runner.py 3 echo hello
```

Вывод: child 0..2: exit=0 time≈0.001s (echo завершается мгновенно).

Родитель форкает N дочерних, каждый через os.execvp заменяет свой образ на
команду, родитель в цикле os.wait() собирает коды возврата. Общее время
работы ≈ времени самого долгого ребёнка (они идут параллельно).

## Задание 3. Зомби и сирота

Зомби (zombie.py — родитель 30 секунд не вызывает wait):

```
python3 zombie.py & sleep 1; ps -eo pid,ppid,stat,cmd | grep defunct
```

Вывод:

```
17839  17837  Z+   [python3] <defunct>
```

Зомби — завершившийся процесс, чей родитель ещё не вызвал wait: запись в таблице
процессов (PID, код возврата) остаётся до wait, это видно как состояние Z.
После os.waitpid зомби исчезает.

Сирота (orphan.py — родитель умирает первым):

```
python3 orphan.py &
ps -o pid,ppid,stat,cmd -p <pid ребёнка>
```

Вывод программы:

```
child 17831 initial PPID = 17830
child 17831 new PPID = 301   (усыновитель)
```

```
ps -p 301 -o pid,ppid,comm=
301   299   Relay(307)
```

Сирота не остаётся без родителя: её усыновляет процесс 301 — Relay (в WSL2 это
роль subreaper'а, в классическом Linux — init с PID 1).

## Задание 4. Ленивое копирование (COW)

```
python3 cow.py
```

Ожидаемый вывод (смотрим Shared_Dirty / Private_Dirty, а не только VmRSS):

```
parent before fork:       RSS=  74588 KB  Shared_Dirty=      0 KB  Private_Dirty=  68804 KB
child right after fork:   RSS=  71728 KB  Shared_Dirty=  68404 KB  Private_Dirty=    420 KB
child after writing:      RSS=  71920 KB  Shared_Dirty=   2708 KB  Private_Dirty=  6616x KB
parent at end:            RSS=  74588 KB  Shared_Dirty=      0 KB  Private_Dirty=  68804 KB
```

Сразу после fork почти весь 64-МБ буфер ребёнка — Shared_Dirty: страницы
физически одни и те же, копирования нет (поэтому fork почти бесплатен).
Как только ребёнок пишет в каждую страницу, ядро копирует её: Shared падает
почти до нуля, Private растёт примерно на размер буфера. Родитель не изменился.
VmRSS почти не растёт, т.к. страницы уже были учтены в RSS как общие —
меняется их тип (общая → личная), а не сумма.

## Выводы
Освоены fork/exec/wait, /proc как источник информации о процессах. Увидены
зомби (нет wait), сироты (усыновление subreaper'ом) и copy-on-write —
механизм, благодаря которому fork дешёвый, а копирование происходит только
при записи.
