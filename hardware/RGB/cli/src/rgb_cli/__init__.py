"""CLI to control the CH552 USB HID 3-LED device.

Protocol: HID Output Report, 1 byte
    bits[1:0] = LED0 state, [3:2] = LED1, [5:4] = LED2
    state: 0 = off, 1 = on, 2 = breathe

No driver install needed — every modern OS speaks HID natively.
"""
from __future__ import annotations

import argparse
import sys

import hid

VID = 0x1209
PID = 0xC552

OFF, ON, BREATHE = 0, 1, 2
STATE_NAMES = {OFF: "off", ON: "on", BREATHE: "breathe"}
NAME_TO_STATE = {v: k for k, v in STATE_NAMES.items()} | {"0": OFF, "1": ON, "2": BREATHE}


def find_device() -> hid.device:
    dev = hid.device()
    try:
        dev.open(VID, PID)
    except OSError as e:
        raise SystemExit(
            f"device {VID:#06x}:{PID:#06x} not found ({e}).\n"
            "Is the board plugged in? Try `rgb info` after replug."
        )
    return dev


def pack(states: list[int]) -> int:
    return (states[0] & 0x3) | ((states[1] & 0x3) << 2) | ((states[2] & 0x3) << 4)


def unpack(raw: int) -> list[int]:
    return [(raw >> (2 * i)) & 0x3 for i in range(3)]


def send_states(dev: hid.device, states: list[int]) -> None:
    raw = pack(states)
    n = dev.write([0x00, raw])
    if n < 0:
        raise SystemExit(f"HID write failed: {dev.error()}")


def get_states(dev: hid.device) -> list[int] | None:
    data = dev.get_feature_report(0, 2)
    if not data:
        return None
    return unpack(int(data[-1]))


def fmt_states(states: list[int]) -> str:
    return ", ".join(f"LED{i}={STATE_NAMES.get(s, '?')}" for i, s in enumerate(states))


def parse_state(text: str) -> int:
    key = text.strip().lower()
    if key not in NAME_TO_STATE:
        raise SystemExit(f"invalid state {text!r}; expected off|on|breathe (or 0|1|2)")
    return NAME_TO_STATE[key]


def parse_indices(values: list[str]) -> list[int]:
    out: list[int] = []
    for v in values:
        try:
            i = int(v)
        except ValueError:
            raise SystemExit(f"invalid LED index: {v!r}")
        if not 0 <= i <= 2:
            raise SystemExit(f"LED index out of range (0..2): {i}")
        out.append(i)
    return out


# ---------------------------------------------------------------- commands


def _apply(args: argparse.Namespace, state: int) -> None:
    targets = parse_indices(args.indices) if args.indices else [0, 1, 2]
    dev = find_device()
    states = [OFF, OFF, OFF]
    for i in targets:
        states[i] = state
    send_states(dev, states)
    print(fmt_states(states))
    dev.close()


def cmd_on(args: argparse.Namespace) -> None:
    _apply(args, ON)


def cmd_off(args: argparse.Namespace) -> None:
    _apply(args, OFF)


def cmd_breathe(args: argparse.Namespace) -> None:
    _apply(args, BREATHE)


def cmd_set(args: argparse.Namespace) -> None:
    """Set each LED individually: `rgb set off on breathe`."""
    if len(args.states) != 3:
        raise SystemExit("set takes exactly 3 states (LED0 LED1 LED2)")
    states = [parse_state(s) for s in args.states]
    dev = find_device()
    send_states(dev, states)
    print(fmt_states(states))
    dev.close()


def cmd_info(_: argparse.Namespace) -> None:
    found = [d for d in hid.enumerate(VID, PID)]
    if not found:
        raise SystemExit(f"device {VID:#06x}:{PID:#06x} not found.")
    for d in found:
        print(f"vid:pid       {d['vendor_id']:#06x}:{d['product_id']:#06x}")
        print(f"manufacturer  {d['manufacturer_string']}")
        print(f"product       {d['product_string']}")
        print(f"serial        {d['serial_number']!r}")
        print(f"release       {d['release_number']:#06x}")
        print(f"path          {d['path'].decode(errors='replace')}")
        print(f"usage_page    {d['usage_page']:#06x}")
        print(f"usage         {d['usage']:#06x}")
        print()


# ---------------------------------------------------------------- entry


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="rgb", description="Control the CH552 HID 3-LED board.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("on", help="turn listed LEDs on, others off; no args = all on")
    sp.add_argument("indices", nargs="*", help="LED indices in 0..2")
    sp.set_defaults(func=cmd_on)

    sp = sub.add_parser("off", help="turn listed LEDs off; no args = all off")
    sp.add_argument("indices", nargs="*", help="LED indices in 0..2")
    sp.set_defaults(func=cmd_off)

    sp = sub.add_parser("breathe", help="set listed LEDs to breathing; no args = all breathe")
    sp.add_argument("indices", nargs="*", help="LED indices in 0..2")
    sp.set_defaults(func=cmd_breathe)

    sp = sub.add_parser("set", help="set per-LED state: `rgb set off on breathe`")
    sp.add_argument("states", nargs=3, help="state for LED0 LED1 LED2: off|on|breathe")
    sp.set_defaults(func=cmd_set)

    sp = sub.add_parser("info", help="show HID device info")
    sp.set_defaults(func=cmd_info)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
