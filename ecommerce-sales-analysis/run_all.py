"""
Master Script - Runs all project steps in sequence.
Usage: python run_all.py
"""
import subprocess
import sys
import os

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "scripts")


def run_script(script_name, description):
    """Run a Python script and print status."""
    print(f"\n{'='*60}")
    print(f"  Running: {description}")
    print(f"{'='*60}")

    script_path = os.path.join(SCRIPTS_DIR, script_name)
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=False,
        text=True
    )

    if result.returncode == 0:
        print(f"\n✅ {description} - SUCCESS")
    else:
        print(f"\n❌ {description} - FAILED")
        return False
    return True


def main():
    """Run all project steps."""
    print("=" * 60)
    print("  E-Commerce Sales Analysis - Complete Pipeline")
    print("=" * 60)

    steps = [
        ("generate_dataset.py", "Step 1: Generate Dataset"),
        ("01_data_preprocessing.py", "Step 2: Data Preprocessing"),
        ("02_eda_visualization.py", "Step 3: EDA & Visualization"),
        ("03_ml_model.py", "Step 4: ML Model Training"),
    ]

    for script, description in steps:
        success = run_script(script, description)
        if not success:
            print(f"\n⚠️ Stopping due to error in {description}")
            return

    print("\n" + "=" * 60)
    print("  ✅ ALL STEPS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\n📊 Outputs:")
    print(f"   Charts: outputs/charts/")
    print(f"   Models: outputs/models/")
    print(f"\n🚀 Next steps:")
    print(f"   1. View charts in outputs/charts/")
    print(f"   2. Check model performance in Step 4 output")
    print(f"   3. Review business insights")


if __name__ == "__main__":
    main()
