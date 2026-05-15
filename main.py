import argparse
from context import *
from commands import *


#commands.get_frekwencja(od="22.04.2026", do="24.04.2026")
#commands.get_sprawdziany(od="04.04.2026", do="15.04.2026")
#commands.get_plan(od="28.04.2026")

parser = argparse.ArgumentParser()

parser.add_argument("type", choices=['uwagi', 'oceny', 'plan', 'sprawdziany', 'frekwencja'])

oceny = parser.add_argument_group('oceny')
oceny.add_argument('--przedmiot', '-p', required=False, default=None, help="wybierz konkretny przedmiot przy 'oceny'")
oceny.add_argument('--okres', '-o', required=False, default=None, help="wybierz konkretny okres klasyfikacyjny przy 'oceny'")

daty = parser.add_argument_group('daty')
daty.add_argument('--od', required=False, default=None, help="wybierz date OD przy 'plan', 'sprawdziany' lub 'frekwencja'")
daty.add_argument('--do', required=False, default=None, help="wybierz date DO przy 'plan', 'sprawdziany' lub 'frekwencja'")

args = parser.parse_args()
print(args)

ctx = Context()
commands = Commands(ctx)

if args.type == 'uwagi':
    commands.get_uwagi();
elif args.type == 'oceny':
    commands.get_oceny(przedmiot=args.przedmiot, okresklasyfikacyjny=args.okres)
elif args.type == 'plan':
    commands.get_plan(od=args.od, do=args.do)
elif args.type == 'sprawdziany':
    commands.get_sprawdziany(od=args.od, do=args.do)
elif args.type == 'frekwencja':
    commands.get_frekwencja(od=args.od, do=args.do)
