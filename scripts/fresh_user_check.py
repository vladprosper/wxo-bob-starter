"""Execute README shell examples in a clean, isolated source distribution."""
import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run():
    with tempfile.TemporaryDirectory(prefix='wxo-fresh-') as temporary:
        work = Path(temporary)/'checkout'
        shutil.copytree(ROOT,work,ignore=shutil.ignore_patterns('.git','.venv','__pycache__','output','*.egg-info'))
        env = Path(temporary)/'venv'
        venv.EnvBuilder(with_pip=False).create(env)
        python = env/('Scripts/python.exe' if sys.platform=='win32' else 'bin/python')
        commands=[]
        for block in re.findall(r'```sh\n(.*?)```',(work/'README.md').read_text(encoding='utf-8'),re.S):
            commands.extend(shlex.split(line) for line in block.splitlines() if line.strip())
        for command in commands:
            assert command[0]=='python3', 'Review new README command before executing'
            command[0]=str(python)
            expected=1 if any('predictions-bad.synthetic' in arg for arg in command) else 0
            r=subprocess.run(command,cwd=work,capture_output=True,text=True,timeout=90)
            assert r.returncode==expected,(command,r.returncode,r.stderr)
            if 'evaluate' in command:
                result=json.loads(r.stdout)
                assert result['matched_cases']==(3 if expected else 6)
            if 'readiness' in command: assert json.loads(r.stdout)['status']=='passed'
        target=Path(temporary)/'my-wxo-project'
        before=(target/'.bob/custom_modes.yaml').read_bytes()
        r=subprocess.run([str(python),'-m','wxo_starter','stage',str(target)],cwd=work,capture_output=True,text=True)
        assert r.returncode==2 and (target/'.bob/custom_modes.yaml').read_bytes()==before
        assert (target/'docs/BOB_ACCEPTANCE.md').exists()
        r=subprocess.run([str(python),'-m','wxo_starter','readiness','examples/readiness/restart.synthetic.json','--as-of','2026-10-20T12:30:00Z'],cwd=work,capture_output=True,text=True)
        assert r.returncode==1 and json.loads(r.stdout)['status']=='failed'
        print(f'Fresh-user check passed: {len(commands)} README commands, repeat-stage refusal, negative readiness; no pip packages installed.')


if __name__=='__main__':
    run()
