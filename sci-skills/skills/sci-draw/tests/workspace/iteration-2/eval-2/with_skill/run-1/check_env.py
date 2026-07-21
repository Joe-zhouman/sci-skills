import sys
print(f"Python: {sys.executable} {sys.version}")
try:
    import matplotlib
    print(f"matplotlib: {matplotlib.__version__}")
except Exception as e:
    print(f"matplotlib FAIL: {e}")
try:
    import seaborn
    print(f"seaborn: {seaborn.__version__}")
except Exception as e:
    print(f"seaborn FAIL: {e}")
try:
    import numpy
    print(f"numpy: {numpy.__version__}")
except Exception as e:
    print(f"numpy FAIL: {e}")
try:
    import pandas
    print(f"pandas: {pandas.__version__}")
except Exception as e:
    print(f"pandas FAIL: {e}")
try:
    import scipy
    print(f"scipy: {scipy.__version__}")
except Exception as e:
    print(f"scipy FAIL: {e}")
try:
    from PIL import Image
    print(f"Pillow: OK")
except Exception as e:
    print(f"Pillow FAIL: {e}")
print("DONE")
