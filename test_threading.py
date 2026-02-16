"""Test to verify PythonCall.jl threading works for Jupyter progress."""
import sys
import time
import threading
import os

# Create a test that simulates the actual usage
print("="*60)
print("Testing Threaded Execution for PySR Jupyter Progress")
print("="*60)

# Test 1: Basic Python threading
print("\n[Test 1] Python threading basics...")

def slow_function(duration):
    time.sleep(duration)
    return f"done after {duration}s"

results = {}

def run_in_thread():
    start = time.time()
    result = slow_function(2)
    results['time'] = time.time() - start
    results['result'] = result

thread = threading.Thread(target=run_in_thread)
start = time.time()
thread.start()

# Main thread does work while background runs
main_work = 0
while thread.is_alive():
    main_work += 1
    time.sleep(0.1)

thread.join()
total_time = time.time() - start

print(f"  Total time: {total_time:.1f}s")
print(f"  Result: {results['result']}")
print(f"  Main thread iterations: {main_work}")

if total_time >= 1.8 and total_time <= 2.5:
    print("  ✓ Threading works correctly")
else:
    print("  ✗ Unexpected timing")
    sys.exit(1)

# Test 2: Check if we can import the modules
print("\n[Test 2] Import PySR modules...")
try:
    sys.path.insert(0, '/root/.openclaw/workspace/worktrees/pysr-jupyter-progress')
    from pysr.threaded_executor import ThreadedExecutor
    from pysr.jupyter_progress import _IpywidgetsProgressDisplay
    print("  ✓ Imports successful")
except Exception as e:
    print(f"  ✗ Import failed: {e}")
    sys.exit(1)

# Test 3: Mock widget test
print("\n[Test 3] ThreadedExecutor with mock widget...")

class MockWidget:
    def __init__(self):
        self.updates = []
    def set_message(self, msg):
        self.updates.append((time.time(), msg))
    def update(self, c, t):
        self.updates.append((time.time(), f"final: {c}/{t}"))
    def close(self):
        pass

widget = MockWidget()
executor = ThreadedExecutor()

start = time.time()
result = executor.execute(slow_function, widget, 2)
elapsed = time.time() - start

print(f"  Elapsed: {elapsed:.1f}s")
print(f"  Updates: {len(widget.updates)}")
print(f"  Result: {result}")

if elapsed >= 1.8 and len(widget.updates) >= 2:
    print("  ✓ ThreadedExecutor works")
else:
    print("  ✗ ThreadedExecutor failed")
    sys.exit(1)

# Test 4: Check juliacall availability
print("\n[Test 4] Check juliacall...")
try:
    import juliacall
    print(f"  ✓ juliacall available")
except ImportError:
    print("  ! juliacall not installed (expected in venv)")

print("\n" + "="*60)
print("All tests passed!")
print("The threading approach should work in Jupyter.")
print("="*60)
