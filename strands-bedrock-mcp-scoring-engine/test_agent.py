#!/usr/bin/env python3
"""
Minimal CLI helper for manually exercising the Strands agent.
Clean output. No chunking. No duplicated prints.
"""

from __future__ import annotations

import json
from typing import Any
from agent import create_agent


EXIT_COMMANDS = {"exit", "quit", "bye", "goodbye"}


def to_text(payload: Any) -> str:
    """Convert anything the agent returns into readable text."""
    if payload is None:
        return "(no response)"

    if isinstance(payload, str):
        return payload

    if isinstance(payload, (bytes, bytearray)):
        return payload.decode(errors="replace")

    try:
        return json.dumps(payload, indent=2, ensure_ascii=False)
    except Exception:
        return str(payload)


def interactive_loop() -> None:
    agent = create_agent()
    print("Interactive Strands agent test. Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if not user_input:
            continue
        if user_input.lower() in EXIT_COMMANDS:
            print("Bye!")
            break

        try:
            response = agent(user_input)   # Only once
        except Exception as exc:
            print(f"[error] {exc}\n")
            continue

        # Print agent response
        print()  # ensure blank line BEFORE next prompt


if __name__ == "__main__":
    interactive_loop()
