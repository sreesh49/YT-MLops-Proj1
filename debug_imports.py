# debug_imports.py
import sys
import traceback

print("Testing imports one by one...")

try:
    print("\n1. Testing src.constants...")
    from src.constants import APP_HOST, APP_PORT
    print(f"   ✓ Success: APP_HOST={APP_HOST}, APP_PORT={APP_PORT}")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    traceback.print_exc()

try:
    print("\n2. Testing src.pipline.prediction_pipeline...")
    from src.pipline.prediction_pipeline import VehicleData
    print("   ✓ Success")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    traceback.print_exc()

try:
    print("\n3. Testing src.pipline.training_pipeline...")
    from src.pipline.training_pipeline import TrainPipeline
    print("   ✓ Success")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    traceback.print_exc()

print("\n" + "="*50)
print("Check your src/__init__.py files if they exist")