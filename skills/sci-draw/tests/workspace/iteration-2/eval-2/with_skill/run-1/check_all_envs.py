import subprocess
import os

envs = {
    'visual': '/opt/local/anaconda3/envs/visual/bin/python',
    'ml': '/opt/local/anaconda3/envs/ml/bin/python',
    'pytorch2': '/opt/local/anaconda3/envs/pytorch2/bin/python',
}

test = 'import matplotlib, seaborn, numpy, pandas, scipy; from PIL import Image; print("ALL OK")'

for name, path in envs.items():
    if os.path.exists(path):
        r = subprocess.run([path, '-c', test], capture_output=True, text=True, timeout=30)
        status = "PASS" if r.returncode == 0 else "FAIL"
        print(f"{status}: {name} ({path})")
        if r.returncode != 0:
            err = r.stderr.strip().split('\n')[-1]
            print(f"  {err}")
