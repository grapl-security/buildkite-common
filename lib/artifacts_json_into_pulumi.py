from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict


def artifacts_json_into_pulumi(
    stack: str,
    input_json: Dict[str, Any],
) -> str:
    return json.dumps(input_json)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stack", type=str)
    parser.add_argument("input_json_path", type=Path)
    args = parser.parse_args()

    with open(args.input_json_path, "r") as file:
        input_json = json.load(file)

    result = artifacts_json_into_pulumi(stack=args.stack, input_json=input_json)
    print(result)


if __name__ == "__main__":
    main()
