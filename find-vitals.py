
from pathlib import Path
import struct

BASE = Path.home() / "bistos-capture/bistos-capture"

FILE = BASE / "capture_20261124_154913/cms_raw.bin"

raw = FILE.read_bytes()

frames = []
offset = 0

while offset + 10 <= len(raw):

    if raw[offset:offset+4] != b"QCMS":
        break

    length = int.from_bytes(
        raw[offset+8:offset+10], "little"
    )

    if length < 10 or offset + length > len(raw):
        break

    packet = raw[offset:offset+length]

    if length == 2518 and packet[7] == 5:
        frames.append(packet)

    offset += length

# Replace with actual monitor readings
targets = {
    "HR": 80,
    "SpO2": 97,
    "PR": 90,
    "RESP": 35
}

print("Frames:", len(frames))

for name, target in targets.items():

    print("\nPARAMETER:", name)
    print("TARGET:", target)

    for pos in range(16, 256):

        for fmt in ("<B", "<h", "<i", "<f"):

            values = [
                struct.unpack_from(fmt, p, pos)[0]
                for p in frames
            ]

            if values and all(
                abs(v - target) < 0.01
                for v in values
            ):
                print(
                    "Offset:", pos,
                    "Format:", fmt,
                    "Values:", values
                )