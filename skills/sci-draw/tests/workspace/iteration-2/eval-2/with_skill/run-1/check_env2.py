import sys
import os
# Try to find a working environment
envs = [
    '/opt/local/anaconda3/envs/autofigure/bin/python',
    '/opt/local/anaconda3/envs/visual/bin/python',
    '/opt/local/anaconda3/envs/ml/bin/python',
]
for env_python in envs:
    if os.path.exists(env_python):
        print(f"Found: {env_python}")
