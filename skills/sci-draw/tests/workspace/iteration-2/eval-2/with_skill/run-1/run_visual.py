"""Wrapper to run a script using the visual env's Python."""
import subprocess
import sys

script = sys.argv[1]
args = sys.argv[2:]
result = subprocess.run(
    ['/opt/local/anaconda3/envs/visual/bin/python', script] + args,
    capture_output=False, text=True
)
sys.exit(result.returncode)
