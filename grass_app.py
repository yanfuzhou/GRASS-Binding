from flask import Flask
from flask_restplus import Resource, Api
import os
import sys
import subprocess
import tempfile
import binascii
import shutil

app = Flask(__name__)
api = Api(app)

myfile = 'sfdem.tif'


@api.route('/grassBinding')
class GrassApp(Resource):
    def get(self):
        grass7bin = os.getenv('GRASS_BIN')
        path = os.getenv('LD_LIBRARY_PATH')
        gisbase = os.getenv('GISBASE')
        os.environ['GISBASE'] = gisbase
        # Todo: If you haven't done following in the terminal
        # Todo: e.g, $ add2virtualenv /usr/local/Cellar/grass7/7.2.0/grass-base/etc/python
        # Todo: please enable below two lines
        # gpydir = os.path.join(gisbase, "etc", "python")
        # sys.path.append(gpydir)
        gisdb = os.path.join(tempfile.gettempdir(), 'grassdata')
        try:
            os.stat(gisdb)
        except:
            os.mkdir(gisdb)
        string_length = 16
        location = binascii.hexlify(os.urandom(string_length))
        mapset = 'PERMANENT'
        location_path = os.path.join(gisdb, location)
        startcmd = grass7bin + ' -c ' + myfile + ' -e ' + location_path
        print startcmd
        try:
            p = subprocess.Popen(startcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
        except OSError as error:
            sys.exit("ERROR: Cannot find GRASS GIS start script"
                     " {cmd}: {error}".format(cmd=startcmd[0], error=error))
        if p.returncode != 0:
            print >> sys.stderr, 'ERROR: %s' % err
            print >> sys.stderr, 'ERROR: Cannot generate location (%s)' % startcmd
            sys.exit(-1)
        else:
            print 'Created location %s' % location_path
        os.environ['GISDBASE'] = gisdb
        dir = os.path.join(gisbase, 'lib')
        if path:
            path = dir + os.pathsep + path
        else:
            path = dir
        os.environ['LD_LIBRARY_PATH'] = path
        os.environ['LANG'] = 'en_US'
        os.environ['LOCALE'] = 'C'
        import grass.script as grass
        import grass.script.setup as gsetup
        gsetup.init(gisbase, gisdb, location, mapset)
        grass.message('--- GRASS GIS 7: Current GRASS GIS 7 environment:')
        print grass.gisenv()
        grass.message('--- GRASS GIS 7: Checking projection info:')
        in_proj = grass.read_command(['g.proj'], flags=['jf'])
        kv = grass.parse_key_val(in_proj)
        print kv
        print kv['+proj']
        in_proj = in_proj.strip()
        grass.message("--- Found projection parameters: '%s'" % in_proj)
        grass.message('--- GRASS GIS 7: Checking computational region info:')
        in_region = grass.region()
        grass.message("--- Computational region: '%s'" % in_region)
        print 'Removing location %s' % location_path
        shutil.rmtree(location_path)
        return {'GRASS': grass.gisenv()}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
