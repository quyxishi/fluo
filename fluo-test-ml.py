from fluo import mlocales
import sys
import re


def main(argc: int, argv: list) -> int:
    fluoin: str = open('fluo.py', 'r', encoding='utf-8').read()
    groups: list = re.findall('''ml\([\"']([a-z]*)[\"']''', fluoin)

    maxsp: int = len(max(groups, key=len)) + 1
    miss = 0
    
    for locale in groups:
        try:
            enlocale: str = getattr(mlocales, 'en_' + locale).strip().replace('\n', '\\n')
        except AttributeError:
            enlocale: str = '\033[1;45mAttributeError\033[0m'
            miss += 1
        
        print(f' ~ en_{locale}{" " * (maxsp - len(locale))}:: {enlocale}')
    
    print(f' * {len(groups) - miss}/{len(groups)}')

if __name__ == '__main__':
    try:
        status: int = main(len(sys.argv), sys.argv)
    except KeyboardInterrupt:
        status: int = 0
    
    sys.exit(status)
