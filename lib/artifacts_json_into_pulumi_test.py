import json
from unittest import TestCase

from lib.artifacts_json_into_pulumi import artifacts_json_into_pulumi

STACK = "some_stack"
EXAMPLE_INPUT = """
{
  "some-service": "some_docker_id",
  "grapl-nomad-consul-client-amis": {
    "us-east-1": "ami-111",
    "us-east-2": "ami-222"
  }
}
"""


class ArtifactsJsonIntoPulumiTests(TestCase):
    def test_basic(self) -> None:
        assert (
            artifacts_json_into_pulumi(
                stack=STACK, input_json=json.loads(EXAMPLE_INPUT)
            )
            == "hey"
        )
