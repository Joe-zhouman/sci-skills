"""Run workflow.py using the visual env's Python."""
import subprocess
import sys

result = subprocess.run(
    ['/opt/local/anaconda3/envs/visual/bin/python',
     '/home/joe/Documents/repo/skill/sci-draw/sci-draw/tests/workspace/iteration-2/eval-2/with_skill/run-1/workflow.py'],
    capture_output=False, text=True
)
sys.exit(result.returncode)
