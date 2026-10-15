
# ПР-1. Диагностическое тестирование. Linux и терминал (вариант B)

Студент: Арсен (limbo). Окружение: Ubuntu 22.04 в WSL2.

## Цель
Развернуть окружение, освоить терминал, пользователей, группы и права доступа.

## Задание 1. Пользователь student2 и группа developers

```
sudo groupadd developers
sudo adduser student2
sudo usermod -aG developers student2
id student2
```

Вывод `id student2`:

```
uid=1001(student2) gid=1002(student2) groups=1002(student2),1001(developers)
```

student2 создан и добавлен в группу developers.

## Задание 2. Каталог /srv/shared

```
sudo mkdir /srv/shared
sudo chown root:developers /srv/shared
sudo chmod 2775 /srv/shared
ls -la /srv
```

Вывод `ls -la /srv`:

```
total 12
drwxr-xr-x  3 root root        4096 Oct 15 21:07 .
drwxr-xr-x 19 root root        4096 Oct 15 19:46 ..
drwxrwsr-x  2 root developers  4096 Oct 15 21:07 shared
```

Права **2775**: 2 = setgid, 7 = rwx владельцу (root), 7 = rwx группе (developers),
5 = r-x остальным. Буква **s** в `rwxrwsr-x` — setgid: новые файлы наследуют
группу каталога (developers), иначе члены группы не смогли бы редактировать
файлы друг друга.

## Задание 3. Файл от student2 и попытка удаления

```
sudo -u student2 touch /srv/shared/test.txt
ls -la /srv/shared
rm -f /srv/shared/test.txt
```

Вывод `ls -la /srv/shared`:

```
total 8
drwxrwsr-x 2 root root        4096 Oct 15 21:10 .
drwxr-xr-x 3 root root        4096 Oct 15 21:07 ..
-rw-rw-r-- 1 student2 developers 0 Oct 15 21:10 test.txt
```

Файл создан от student2, а группа у файла — **developers**: setgid сработал.

Результат удаления от основного пользователя (limbo):

```
rm: cannot remove '/srv/shared/test.txt': Permission denied
```

Объяснение: удаление файла — это право на **запись в каталог**, а не на сам файл.
Каталог принадлежит root:developers, я (limbo) для него «others» с правами
r-x — права на запись нет. Поэтому удалить чужой файл нельзя, даже если бы
права на файл были 777. (Без `-f` rm сперва спрашивает «remove write-protected
file?» — вопрос про права на сам файл, а удалять всё равно не даёт.)

## Задание 4. su vs sudo и блокировка root

**su** переключает пользователя целиком: требует пароль ЦЕЛЕВОГО пользователя
(root) и открывает его полную сессию до команды exit.
**sudo** выполняет одну команду от root: требует МОЙ пароль, root-сессия не
открывается, каждый вызов логируется в /var/log/auth.log.

Root в Ubuntu заблокирован по умолчанию, потому что:
- все админские действия привязаны к конкретному пользователю (аудит);
- окно с максимальными правами минимально (одна команда, а не сессия);
- вход под root по SSH запрещён;
- пароль root вообще не задан (в /etc/shadow стоит "!").

## Задание 5. Алиасы в ~/.bashrc

Добавлено в конец ~/.bashrc:

```bash
alias ll='ls -la'
alias cls='clear'
export COURSE_DIR=~/os-course
```

Проверка в новой сессии (`bash -l`): `ll` выводит длинный список файлов,
`echo $COURSE_DIR` выводит:

```
/home/limbo/os-course
```

Новая сессия обязательна: .bashrc читается при старте интерактивной оболочки,
уже открытый терминал старую версию не перечитывает.

## Выводы
Освоены команды терминала, создание пользователей и групп, назначение прав
(chown, chmod, setgid), настроено окружение (git, python3, gcc, strace),
код сдаётся через GitHub (github.com/Limbovsk1/os-course).
