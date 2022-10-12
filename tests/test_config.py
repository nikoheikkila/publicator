from pathlib import Path
from unittest.mock import MagicMock

from publicator.config import Configuration, NullConfiguration, factory


class TestConfig:
    def test_factory_resolves_to_real_configuration(self, mock_read_text: MagicMock) -> None:
        mock_read_text.return_value = "[tool.publicator]"

        configuration = factory("pyproject.toml")

        assert isinstance(configuration, Configuration)

    def test_factory_resolves_to_null_configuration_on_missing_file(self, tmp_path: Path) -> None:
        filename = tmp_path / "missing.toml"

        configuration = factory(filename.as_posix())

        assert isinstance(configuration, NullConfiguration)

    def test_factory_resolves_to_null_configuration_on_missing_section(self, mock_read_text: MagicMock) -> None:
        mock_read_text.return_value = "[tool.poetry]"

        configuration = factory("pyproject.toml")

        assert isinstance(configuration, NullConfiguration)

    def test_get_from_configuration(self, mock_read_text: MagicMock) -> None:
        mock_read_text.return_value = """
        [tool.publicator]
        repository = "pypi"
        """

        configuration = Configuration.from_path(Path("config.toml"))

        assert configuration.get("repository") == "pypi"

    def test_get_from_null_configuration(self) -> None:
        configuration = NullConfiguration.from_path(Path("config.toml"))

        assert configuration.get("key") is None
        assert configuration.get("key", "value") == "value"
