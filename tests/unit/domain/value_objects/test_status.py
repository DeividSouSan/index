"""Testes unitários para o Value Object Status."""

import pytest

from index_tui.domain.value_objects import Status


class TestStatusValid:
    """Cenários válidos do Status."""

    def test_create_ok_status(self):
        status = Status("OK")

        assert status.value == "OK"
        assert str(status) == "OK"
        assert status.is_ok() is True
        assert status.is_nok() is False

    def test_create_nok_status(self):
        status = Status("NOK")

        assert status.value == "NOK"
        assert str(status) == "NOK"
        assert status.is_ok() is False
        assert status.is_nok() is True


class TestStatusInvalid:
    """Cenários inválidos do Status."""

    @pytest.mark.parametrize(
        "invalid_value",
        [
            "ok",
            "Ok",
            "nok",
            "Nok",
            " OK",
            "OK ",
            "NOK ",
            "",
            " ",
            "PENDING",
            "UNKNOWN",
        ],
    )
    def test_rejects_invalid_string_values(self, invalid_value):
        with pytest.raises(ValueError):
            Status(invalid_value)

    @pytest.mark.parametrize("invalid_value", [None, 1, 0, True, False, [], {}, ("OK",)])
    def test_rejects_non_string_values_with_type_error(self, invalid_value):
        with pytest.raises(TypeError):
            Status(invalid_value)
