import subprocess

from django.db.backends.base.client import BaseDatabaseClient


class CassandraDatabaseClient(BaseDatabaseClient):
    executable_name = 'cqlsh'

    def runshell(self):
        settings_dict = self.connection.settings_dict
        args = [self.executable_name]
        if settings_dict['HOST']:
            args.extend([settings_dict['HOST'].split(',')[0]])
        if settings_dict['PORT']:
            args.extend([str(settings_dict['PORT'])])
        if settings_dict['USER']:
            args += ["-u", settings_dict['USER']]
        args += ["-k", settings_dict['NAME']]

        subprocess.call(args)
