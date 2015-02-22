import io
import os
import struct
import sys
import sysconfig

from zipfile import ZipFile

import pkg_resources


def in_venv():
    if hasattr(sys, 'real_prefix'):
        # virtualenv venvs
        result = True
    else:
        # PEP 405 venvs
        result = sys.prefix != getattr(sys, 'base_prefix', sys.prefix)
    return result


def get_shebang(gui=False):
    if not sysconfig.is_python_build():
        executable = sys.executable
    elif in_venv():
        executable = os.path.join(sysconfig.get_path('scripts'),
                        'python%s' % sysconfig.get_config_var('EXE'))
    else:
        executable = os.path.join(
            sysconfig.get_config_var('BINDIR'),
            'python%s%s' % (sysconfig.get_config_var('VERSION'),
                            sysconfig.get_config_var('EXE')))
    if gui and os.name == 'nt':
        dn, fn = os.path.split(executable)
        fn = fn.replace('python', 'pythonw')
        executable = os.path.join(dn, fn)
    # For executable paths with spaces (not uncommon on Windows)
    if ' ' in executable:
        executable = '"%s"' % executable
    executable = executable.encode('utf-8')
    return b'#!' + executable + b'\n'


def get_launcher(gui):
    """Use the exe files generated via
    https://bitbucket.org/vinay.sajip/simple_launcher"""
    if struct.calcsize('P') == 8:   # 64-bit
        bits = '64'
    else:
        bits = '32'
    name = 'launchers/%s%s.exe' % ('w' if gui else 't', bits)
    data = pkg_resources.ResourceManager().resource_stream('scriptlib', name)
    return data.read()


def get_global_script_bytes(shebang, script_bytes, gui=False):
    linesep = os.linesep.encode('utf-8')
    if os.name != 'nt':
        return shebang + linesep + script_bytes
    else:
        launcher = get_launcher(gui)
        stream = io.BytesIO()
        with ZipFile(stream, 'w') as zf:
            zf.writestr('__main__.py', script_bytes)
        zip_data = stream.getvalue()
        return launcher + shebang + linesep + zip_data


def write_script(target_filename, shebang, script_bytes, gui=False):
    script_bytes = get_global_script_bytes(shebang, script_bytes, gui)

    outname = os.path.join(target_filename)
    if os.name == 'nt':
        outname_noext, ext = os.path.splitext(outname)
        if ext.startswith('.py'):
            outname = outname_noext
        outname = '%s.exe' % outname
        try:
            with open(outname, 'wb') as f:
                f.write(script_bytes)
        except Exception:
            # cf https://mail.python.org/pipermail/distutils-sig/2013-August/022263.html
            dfname = '%s.deleteme' % outname
            if os.path.exists(dfname):
                os.remove(dfname)       # Not allowed to fail here
            os.rename(outname, dfname)  # nor here
            with open(outname, 'wb') as f:
                f.write(script_bytes)
            try:
                os.remove(dfname)
            except Exception:
                pass    # still in use - ignore error
    else:
        with open(outname, 'wb') as f:
            f.write(script_bytes)
        if os.name == 'posix':
            mode = (os.stat(outname).st_mode | 0o555) & 0o7777
            os.chmod(outname, mode)
    return outname
