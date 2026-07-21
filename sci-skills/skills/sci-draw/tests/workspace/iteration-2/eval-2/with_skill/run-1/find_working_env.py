import subprocess
import os

envs = [
    '/opt/local/anaconda3/envs/autofigure/bin/python',
    '/opt/local/anaconda3/envs/visual/bin/python',
    '/opt/local/anaconda3/envs/ml/bin/python',
    '/opt/local/anaconda3/envs/pytorch2/bin/python',
    '/opt/local/anaconda3/envs/mineru/bin/python',
    '/home/joe/.conda/envs/p4dev/bin/python',
]

test_code = 'import matplotlib, seaborn, numpy, pandas; from PIL import Image; print("OK")'

for env_python in envs:
    if os.path.exists(env_python):
        result = subprocess.run(
            [env_python, '-c', test_code],
            capture_output=True, text=True, timeout=30
        )
        status = "PASS" if result.returncode == 0 else "FAIL"
        print(f"{status}: {env_python}")
        if result.returncode == 0:
            print(f"  Output: {result.stdout.strip()}")
        else:
            err = result.stderr.strip().split('\n')[-1] if result.stderr else "unknown"
            print(f"  Error: {err}")
