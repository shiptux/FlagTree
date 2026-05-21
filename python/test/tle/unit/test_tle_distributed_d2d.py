import triton.experimental.tle.language as tle
import torch
import triton
import triton.language as tl

DEVICE_MESH = tle.device_mesh(tle.MeshConfig(device=2))


@triton.jit
def _remote_peer_d2d_kernel(in_ptr, out_ptr, mesh: tl.constexpr, BLOCK: tl.constexpr):

    remote_mem = tle.remote(in_ptr, space="device", shard_id=0)
    x = tl.load(remote_mem)
    tl.store(out_ptr, x)


class TestDeviceToDevice:

    def test_tle_d2d_remote(self):
        block = 64
        grid = 2
        x = torch.randn([1024, 1024], device="cuda", dtype=torch.float32)
        y = torch.empty_like(x)

        compiled = _remote_peer_d2d_kernel.warmup(
            in_ptr=x,
            out_ptr=y,
            mesh=DEVICE_MESH,
            BLOCK=block,
            grid=(grid, ),
            num_ctas=1,
            num_warps=4,
        )
        assert "remote_pointers" in compiled.asm["ttgir"]
        assert "flagcxGetIntraPointerC" in compiled.asm['ptx']

        _remote_peer_d2d_kernel[(grid, )](in_ptr=x, out_ptr=y, mesh=DEVICE_MESH, BLOCK=block)
