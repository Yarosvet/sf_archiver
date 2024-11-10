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
        if args['mode'] == 'gui' or args['mode'] is None:
            self.gui_callback()
        elif args['mode'] == 'compress':
            self.compress_callback(args['input'], args['output'], bool(args['verify']), args['algorithm'])
        elif args['mode'] == 'decompress':
            self.decompress_callback(args['input'], args['output'], bool(args['verify']))
