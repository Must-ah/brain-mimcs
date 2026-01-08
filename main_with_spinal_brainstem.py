from __future__ import annotations

import argparse
import asyncio
import importlib
import sys
from pathlib import Path


# Ensure `src/` is on the module search path when running `python main.py`.
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


# Allowlist of modules that can be imported via _import_optional
_ALLOWED_MODULES: frozenset[str] = frozenset([
    "cerebrum.subcortical.hypothalamus.hypothalamus_async",
    "cerebrum.subcortical.basal_ganglia.basal_ganglia_async",
    "cerebrum.subcortical.limbic.limbic_interface_skeleton_aligned_async",
    "cerebrum.cortex.mock_cortex_async",
    "communication.communication_contracts_async_v2",
    "shared.contracts_base_async",
    "shared.topics_async",
    "spinal_cord.spinal_contracts_async_refactored_v2",
    "brainstem.brainstem_contracts_async_refactored_v2",
])


def _import_optional(module_name: str) -> None:
    """Import a module and print a friendly message if it's missing.

    Only modules in the allowlist can be imported for security.
    """
    if module_name not in _ALLOWED_MODULES:
        print(f"[error] module {module_name} not in allowlist")
        return
    try:
        importlib.import_module(module_name)
        print(f"[ok] imported {module_name}")
    except ImportError as e:
        print(f"[warn] could not import {module_name}: {e}")
    except Exception as e:
        print(f"[error] unexpected error importing {module_name}: {type(e).__name__}: {e}")


async def run_demo_mock_cortex() -> None:
    from cerebrum.cortex.mock_cortex_async import demo_mock_cortex_roundtrip
    await demo_mock_cortex_roundtrip()


async def run_demo_comms_router() -> None:
    from communication.communication_contracts_async_v2 import demo_router
    await demo_router()


async def run_demo_spinal_brainstem() -> None:
    from demo_spinal_brainstem import demo_spinal_brainstem
    await demo_spinal_brainstem()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run async demos for the brain-inspired interface skeletons."
    )
    parser.add_argument(
        "--demo",
        choices=["mock-cortex", "comms-router", "spinal-brainstem"],
        default="mock-cortex",
        help="Which demo to run.",
    )

    args = parser.parse_args(argv)

    # Sanity imports for your current tree structure
    _import_optional("cerebrum.subcortical.hypothalamus.hypothalamus_async")
    _import_optional("cerebrum.subcortical.basal_ganglia.basal_ganglia_async")
    _import_optional("cerebrum.subcortical.limbic.limbic_interface_skeleton_aligned_async")
    _import_optional("cerebrum.cortex.mock_cortex_async")

    # Communication contracts
    _import_optional("communication.communication_contracts_async_v2")

    # Pattern A (canonical v2) sanity imports
    _import_optional("shared.contracts_base_async")
    _import_optional("shared.topics_async")
    _import_optional("spinal_cord.spinal_contracts_async_refactored_v2")
    _import_optional("brainstem.brainstem_contracts_async_refactored_v2")

    # Demos
    if args.demo == "mock-cortex":
        asyncio.run(run_demo_mock_cortex())
        return 0

    if args.demo == "comms-router":
        asyncio.run(run_demo_comms_router())
        return 0

    if args.demo == "spinal-brainstem":
        asyncio.run(run_demo_spinal_brainstem())
        return 0

    print("No runnable demo selected.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
