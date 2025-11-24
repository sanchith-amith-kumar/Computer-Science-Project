import subprocess
import os
from typing import Tuple

def run_command(cmd, cwd=None) -> Tuple[int, str, str]:
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, text=True)
    out, err = p.communicate()
    return p.returncode, out, err

class Validator:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def validate(self):
        cwd = os.path.abspath(self.output_dir)
        cmds = [
            ['terraform', 'fmt', '-check'],
            ['terraform', 'init', '-backend=false'],
            ['terraform', 'validate']
        ]
        results = []
        for cmd in cmds:
            rc, out, err = run_command(cmd, cwd=cwd)
            results.append({'cmd': ' '.join(cmd), 'rc': rc, 'out': out, 'err': err})
            if rc != 0:
                # stop on first failure
                break
        return results
