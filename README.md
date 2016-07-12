Утилита для автоматической разборки *epf*-, *erf*-, *ert*- и *md*-файлов при помещении (committing) в git-репозиторий
===

Что делает
---

*epf*- и *erf*-файлы автоматически разбираются с помощью [v8Reader](https://github.com/xDrivenDevelopment/v8Reader), а 
*ert*-и *md*-файлы — с помощью [GComp](http://1c.alterplast.ru/gcomp/). Результат разбора добавляется в индекс и 
помещается в git-репозиторий.

Требования
---

- Windows
- Python 3.5. Каталоги интерпретатора и скриптов Python должны быть прописаны в переменной окружения Path
- Пакет [decompiler1cwrapper](https://github.com/Cujoko/decompiler1cwrapper) с необходимыми настройками

Состав
---

- *precommit1c.py* — cобственно скрипт
- *pre-commit.sample* — образец hook-скрипта, запускающего *pre-commit-1c.bat*
- *pre-commit-1c.bat* — *bat*-скрипт, ищущий в переменной окружения Path путь до *precommit1c.exe* и запускающий его
- *createlinksinhooks.py* — скрипт, создающий символические ссылки в *.git/hooks* проекта на 
*pre-commit.sample* (c именем *pre-commit*) и *pre-commit-1c.bat*

Установка
---

Вы можете собрать пакет, запустив *setup.py* с ключом sdist. После чего в каталоге *dist* проекта появится *zip*-архив 
пакета, установить который можно запустив:

> pip install <архив>

После установки в каталоге скриптов интерпретатора Python появится файл *clihp.exe*, который предназначен для быстрого 
создания в каталоге *.git\\hooks* репозитория символических ссылок на необходимые для работы утилиты файлы. Запускать 
его нужно из каталога репозитория.