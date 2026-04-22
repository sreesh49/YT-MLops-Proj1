# debug_jinja.py
import sys
import os

print("Step 1: Import FastAPI and Jinja2")
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

print("Step 2: Create templates directory")
templates_dir = os.path.join(os.getcwd(), "templates")
print(f"Templates dir: {templates_dir}")
print(f"Exists: {os.path.exists(templates_dir)}")

print("Step 3: Create Jinja2Templates")
try:
    templates = Jinja2Templates(directory=templates_dir)
    print("✓ Jinja2Templates created successfully")
except Exception as e:
    print(f"✗ Failed: {e}")

print("\nStep 4: Try to get a template")
try:
    template = templates.get_template("vehicledata.html")
    print("✓ Template loaded successfully")
except Exception as e:
    print(f"✗ Failed: {e}")
    import traceback
    traceback.print_exc()

print("\nStep 5: Import your modules one by one")
modules_to_test = [
    'src.constants',
    'src.pipline.prediction_pipeline',
    'src.pipline.training_pipeline'
]

for module_name in modules_to_test:
    print(f"\nImporting {module_name}...")
    try:
        __import__(module_name)
        print(f"✓ {module_name} imported")
        
        # Try to use templates again after import
        try:
            template = templates.get_template("vehicledata.html")
            print(f"  ✓ Template still works after importing {module_name}")
        except Exception as e:
            print(f"  ✗ Template BROKEN after importing {module_name}: {e}")
            break
    except Exception as e:
        print(f"✗ Failed to import {module_name}: {e}")