def precompile_hook(*args, **kargs):
    default_backends = kargs['default_backends']
    default_backends.append('triton_shared')


def compile_flagcx(*args, **kargs):
    import subprocess
    from pathlib import Path
    flagcx_dir = kargs['backend'].dst_path
    bitcode_path = Path(flagcx_dir) / "build" / "lib" / "libflagcx_device.bc"
    if bitcode_path.exists():
        print("libflagcx_device.bc already exists, skipping compilation.")
    else:
        print(f"Compiling libflagcx_device.bc in {flagcx_dir}...")
        subprocess.run(["make", "-C", "bindings/ir/nvidia"], cwd=flagcx_dir, check=True)
        if not bitcode_path.exists():
            raise FileNotFoundError(f"Expected bitcode file not found: {bitcode_path}")

        print("libflagcx_device.bc compilation completed.")
