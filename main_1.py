from __future__ import annotations

import argparse
import asyncio
import importlib
import sys


def _import_optional(module_name: str) -> None:
    """Import a module and print a friendly message if it's missing."""
    try:
        importlib.import_module(module_name)
        print(f"[ok] imported {module_name}")
    except Exception as e:
        print(f"[warn] could not import {module_name}: {e}")


async def run_demo_mock_cortex() -> None:
    # The mock cortex module includes a self-contained demo coroutine.
    from mock_cortex_async import demo_mock_cortex_roundtrip
    await demo_mock_cortex_roundtrip()


async def run_demo_comms_router() -> None:
    # The communication contracts module includes a demo router coroutine.
    from communication_contracts_async import demo_router
    await demo_router()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run async demos for the brain-inspired interface skeletons."
    )
    parser.add_argument(
        "--demo",
        choices=["mock-cortex", "comms-router"],
        default="mock-cortex",
        help="Which demo to run.",
    )

    args = parser.parse_args(argv)

    # Sanity imports (these are skeletons; importability helps verify packaging)
    _import_optional("hypothalamus_async")
    _import_optional("basal_ganglia_async")
    _import_optional("limbic_interface_skeleton_aligned_async")
    _import_optional("mock_cortex_async")
    _import_optional("communication_contracts_async")

    if args.demo == "mock-cortex":
        asyncio.run(run_demo_mock_cortex())
        return 0

    if args.demo == "comms-router":
        asyncio.run(run_demo_comms_router())
        return 0

    print("No runnable demo selected.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
