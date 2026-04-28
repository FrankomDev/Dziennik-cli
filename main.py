from context import *
from commands import *

ctx = Context()
commands = Commands(ctx)

#commands.get_frekwencja(od="22.04.2026", do="24.04.2026")
#commands.get_sprawdziany(od="04.04.2026", do="15.04.2026")
commands.get_plan(od="28.04.2026")
