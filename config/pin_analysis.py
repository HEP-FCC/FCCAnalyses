'''
The module pins/unpins FCCAnalyses to the current version of the Key4hep stack
'''

import os
import sys
import pathlib


class PinAnalysis:
    '''
    Pin/unpin FCCAnalyses to the current version of the Key4hep stack
    '''
    def __init__(self, mainparser):
        '''
        Setup analysis pinning
        '''

        if 'LOCAL_DIR' not in os.environ:
            print('----> Error: FCCAnalyses environment not set up correctly!')
            print('      Aborting...')
            sys.exit(3)

        self.local_dir = os.environ.get('LOCAL_DIR')
        self.pin_path = pathlib.Path(self.local_dir + '/.fccana/stackpin')

        self.args, _ = mainparser.parse_known_args()

        if self.args.show:
            self.show_pin()

        if self.args.clear:
            self.unpin_analysis()
        else:
            self.pin_analysis()

    def show_pin(self):
        '''
        Show current pin
        '''
        if not self.pin_path.is_file():
            print('----> Info: Analysis not pinned.')
            sys.exit(0)

        with open(self.pin_path, 'r') as pinfile:
            lines = pinfile.readlines()

            if len(lines) != 1:
                print('----> Error: Analysis pin file malformed!')
                sys.exit(3)

            stack_path = lines[0]

            print('----> Analysis pinned to the following Key4hep stack:')
            print('      ' + stack_path)

        sys.exit(0)

    def unpin_analysis(self):
        '''
        Unpin analysis from any Key4hep stack version
        '''
        if not self.pin_path.is_file():
            print('----> Warning: Analysis pin file not found!')
            sys.exit(0)

        print('----> Unpinning analysis located in:')
        print('      ' + self.local_dir)
        self.pin_path.unlink()

        with os.scandir(os.path.dirname(self.pin_path)) as item:
            if any(item):
                sys.exit(0)
        os.rmdir(os.path.dirname(self.pin_path))

        sys.exit(0)

    def pin_analysis(self):
        '''
        Pin analysis to the Key4hep stack version
        '''
        if self.pin_path.is_file() and not self.args.force:
            print('----> Warning: Analysis pin file already created!')
            print('      Use "--force" flag to overwrite current pin.')
            print('      Aborting...')
            sys.exit(0)

        if 'KEY4HEP_STACK' not in os.environ:
            print('----> Error: FCCAnalyses environment not set up correctly!')
            print('      Aborting...')
            sys.exit(3)

        stack_path = os.environ.get('KEY4HEP_STACK')

        print('----> Pinning analysis located in:')
        print('      ' + self.local_dir)
        print('      to Key4hep stack:')
        print('      ' + stack_path)

        os.makedirs(os.path.dirname(self.pin_path), exist_ok=True)

        with open(self.pin_path, 'w') as pinfile:
            pinfile.write(stack_path + '\n')

        sys.exit(0)
