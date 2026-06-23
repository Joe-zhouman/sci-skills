import subprocess
import sys

result = subprocess.run(
    ['/opt/local/anaconda3/envs/autofigure/bin/python', '-c',
     'import matplotlib, seaborn, numpy, pandas, scipy; from PIL import Image; print("OK")'],
    capture_output=True, text=True
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)
