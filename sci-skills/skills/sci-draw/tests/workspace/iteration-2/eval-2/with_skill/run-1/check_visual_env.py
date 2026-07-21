import subprocess
result = subprocess.run(
    ['/opt/local/anaconda3/envs/visual/bin/python', '-c',
     'import matplotlib, seaborn, numpy, pandas; print("core OK"); '
     'import scipy; print("scipy OK")'],
    capture_output=True, text=True
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr[-500:] if result.stderr else "")
print("Return code:", result.returncode)
