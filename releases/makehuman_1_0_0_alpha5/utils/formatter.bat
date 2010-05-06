astyle  --style=ansi  ../src/main.c  ../src/core.c ../src/glmodule.c ../include/core.h ../include/glmodule.h

for %%X in (../mh_core/*.py) do pythontidy.py ../mh_core/%%X ../mh_core/%%X
for %%X in (../mh_plugins/*.py) do pythontidy.py ../mh_plugins/%%X ../mh_plugins/%%X
for %%X in (../plugins/*.py) do pythontidy.py ../plugins/%%X ../plugins/%%X