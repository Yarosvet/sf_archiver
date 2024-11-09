from sf_app.misc import SimpleCallback

from .parser import configure_parser


class CommandLineInterface:

    def __init__(self):
        self.compress_callback = SimpleCallback()
        self.decompress_callback = SimpleCallback()
        self.gui_callback = SimpleCallback()

    def run(self):
        _parser = configure_parser()
        args = vars(_parser.parse_args())
        if args['mode'] == 'compress':
            self.compress_callback(args['input'], args['output'])
        elif args['mode'] == 'decompress':
            self.decompress_callback(args['input'], args['output'])
        elif args['mode'] == 'gui':
            self.gui_callback()
