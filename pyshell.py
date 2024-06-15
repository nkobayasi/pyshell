

ShellResults = collections.namedtuple('ShellResults', ['stdout', 'stderr'])
class Shell(object):
    def __init__(self, timeout=60):
        self.timeout = timeout
    
    def get_locale(self):
        return locale.getdefaultlocale()
    
    @property
    def encoding(self):
        return self.get_locale()[1].lower()

    def execute(self, command, stdin=None, shell=False):
        if isinstance(command, str):
            command = shlex.split(command)
        if shell:
            command = ['/bin/sh', '-c', shlex.join(command)]
        p = subprocess.run(command, input=stdin.encode(self.encoding) if stdin else None, timeout=self.timeout, capture_output=True)
        p.check_returncode()
        return ShellResults(
            p.stdout.decode(self.encoding).rstrip('\n'),
            p.stderr.decode(self.encoding).rstrip('\n'))

    def sudo(self, command, stdin=None, shell=True):
        if isinstance(command, list):
            command = shlex.join(command) 
        if shell:
            command = ['sudo', '/bin/sh', '-c', command]
        else:
            command = ['sudo', command]
        return self.execute(command, stdin)
