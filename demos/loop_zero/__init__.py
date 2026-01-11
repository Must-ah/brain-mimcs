"""
Loop Zero - Concurrent Proof-of-Concept Demo

This package contains a minimal demonstration of the brain-mimc
concurrent architecture. It proves that Cortex, Thalamus, and TRN
can run as separate processes communicating via MQTT without blocking.

Files:
- loop_zero_contracts.py: Minimal contracts (ThalamicEnvelope, GateState)
- loop_zero_cortex.py: Cortex process (L4 receive, L5 send)
- loop_zero_thalamus.py: Thalamus process (relay with gating)
- loop_zero_trn.py: TRN process (gate control)
- run_loop_zero.sh: Runner script

Usage:
    ./run_loop_zero.sh          # Start all processes
    ./run_loop_zero.sh stop     # Stop all processes
    ./run_loop_zero.sh status   # Show running processes
"""
