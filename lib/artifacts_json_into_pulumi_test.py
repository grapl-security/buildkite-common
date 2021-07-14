import json
from unittest import TestCase

from lib.artifacts_json_into_pulumi import _artifacts_json_into_pulumi

STACK = "some_stack"
CWD = "some_cwd"
EXAMPLE_INPUT = """
{
  "some-service": "some_docker_id",
  "some-amis": {
    "us-east-1": "ami-111",
    "us-east-2": "ami-222"
  },
  "some-bool": true,
  "some-int": 123
}
"""
EXPECTED_OUTPUT = [
    'pulumi config set --path "artifacts.some-service" "some_docker_id" --cwd=some_cwd --stack=some_stack',
    'pulumi config set --path "artifacts.some-amis.us-east-1" "ami-111" --cwd=some_cwd --stack=some_stack',
    'pulumi config set --path "artifacts.some-amis.us-east-2" "ami-222" --cwd=some_cwd --stack=some_stack',
    'pulumi config set --path "artifacts.some-bool" "true" --cwd=some_cwd --stack=some_stack',
    'pulumi config set --path "artifacts.some-int" "123" --cwd=some_cwd --stack=some_stack',
]


class ArtifactsJsonIntoPulumiTests(TestCase):
    def test_basic(self) -> None:
        actual = list(
            _artifacts_json_into_pulumi(
                input_json=json.loads(EXAMPLE_INPUT),
                stack=STACK,
                cwd=CWD,
            )
        )

        assert EXPECTED_OUTPUT == actual
