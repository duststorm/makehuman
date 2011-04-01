astyle  --style=ansi  ../src/main.c  ../src/core.c ../src/glmodule.c ../include/core.h ../include/glmodule.h

for %%X in (../core/*.py) do pythontidy.py ../core/%%X ../core/%%X
for %%X in (../apps/*.py) do pythontidy.py ../apps/%%X ../apps/%%X
for %%X in (../plugins/*.py) do pythontidy.py ../plugins/%%X ../plugins/%%X