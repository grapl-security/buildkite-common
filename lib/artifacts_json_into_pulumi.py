#!/usr/bin/python3
"""
The purpose of this module is to convert something like the following json:
{
  "some-service": "some_docker_id",
  "some-amis": {
    "us-east-1": "ami-111",
    "us-east-2": "ami-222"
  }
}

into valid `pulumi config set` keys, like:
pulumi config set --path "artifacts.some-service" "some_docker_id" --cwd=pulumi/cicd --stack=grapl/production
pulumi config set --path "artifacts.some-amis.us-east-1" "ami-111" --cwd=pulumi/cicd --stack=grapl/production
pulumi config set --path "artifacts.some-amis.us-east-2" "ami-222" --cwd=pulumi/cicd --stack=grapl/production
"""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict, Iterable, List, NamedTuple

JsonDict = Dict[str, Any]
PulumiKVPair = NamedTuple(
    "PulumiKVPair",
    (("key", str), ("value", str)),  # pulumi autoconverts "true", "false", "123" for us
)


def _get_key_values_recursive(
    keys_to_here: List[str],
    curr: Any,  # dict or primitive
) -> Iterable[PulumiKVPair]:
    """
    spit out tuples of ("artifacts.some-amis.us-east-2", "ami-222")
    """
    if isinstance(curr, dict):
        for (k, v) in curr.items():
            assert (
                "." not in k
            ), "Can't use a period in a key - reserved in Pulumi as a  delim"
            # re-yield things from our recurse
            yield from _get_key_values_recursive([*keys_to_here, k], v)
    elif isinstance(curr, list):
        raise Exception("TODO")
    elif isinstance(curr, (int, bool, str)):
        # deals with `True` becoming `true`, among oher things
        if isinstance(curr, bool):
            curr = str(curr).lower()
        yield PulumiKVPair(key=".".join(keys_to_here), value=curr)
    else:
        raise Exception(f"Unhandled object {curr}")


def _artifacts_json_into_pulumi(
    input_json: JsonDict,
    stack: str,
    cwd: str,
) -> Iterable[str]:
    # prepend all of these with `artifacts.`
    assert isinstance(input_json, dict), f"expected dict, got {type(input_json)}"
    kv_pairs = _get_key_values_recursive(keys_to_here=["artifacts"], curr=input_json)
    for (k, v) in kv_pairs:
        yield f'pulumi config set --path "{k}" "{v}" --cwd={cwd} --stack={stack}'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stack", type=str)
    parser.add_argument("--cwd", type=str)
    parser.add_argument(
        "--input_json", type=str, help="input json string (not a path or anything)"
    )
    args = parser.parse_args()

    for command in _artifacts_json_into_pulumi(
        stack=args.stack, cwd=args.cwd, input_json=json.loads(args.input_json)
    ):
        print(command)


if __name__ == "__main__":
    main()
