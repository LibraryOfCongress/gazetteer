from django.core.management.base import BaseCommand, CommandError
import subprocess
from os.path import join
from gazetteer import settings

class Command(BaseCommand):
    help = 'Minify and build JS files (requires r.js)'

    def handle(self, *args, **options):
        build_file_path = join(settings.PROJECT_ROOT, '../static/js', 'app.build.js')
        self.stdout.write("Building %s .. please wait .."%build_file_path)
        build_process = subprocess.Popen(['node_modules/requirejs/bin/r.js', '-o', build_file_path], stdout=subprocess.PIPE)
        for line in build_process.stdout:
            self.stdout.write(line)
        #self.stdout.write("Done minifying JS")
