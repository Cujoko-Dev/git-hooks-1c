Смысл всего этого в том, что при коммите epf- и erf-файлы автоматически распаковываться с помощью 
[V8Reader](https://github.com/xDrivenDevelopment/v8Reader), а ert- и md-файлы — с помощью 
[GComp](http://1c.alterplast.ru/gcomp/). Результат распаковки добавляется в индекс и коммитится.

Пути к платформе 1С:Предприятия 8, сервисной информационной базе, V8Reader.epf и GComp следует указать в файле настроек 
pre-commit-1c.ini, который сначала ищется в каталоге проекта, а потом в каталоге со скриптом (то есть в hooks).

create-links-in-hooks.bat (или copy-files-to-hooks.bat, если вдруг создание символических ссылок невозможно) нужно 
запускать из каталога проекта.
