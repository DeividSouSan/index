"""Value Object para Status."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Status:
    """Value Object para representar o status de um artigo.

    Status válidos: OK, NOK
    """

    VALID_VALUES = {"OK", "NOK"}
    value: str

    def __post_init__(self) -> None:
        """Valida o status no momento da criação."""
        if not isinstance(self.value, str):
            raise TypeError("Status deve ser uma string.")

        if self.value not in self.VALID_VALUES:
            raise ValueError(f"Status inválido: {self.value}. Deve ser um de {self.VALID_VALUES}")

    def __str__(self) -> str:
        """Representação textual do status."""
        return self.value

    def is_ok(self) -> bool:
        """Verifica se o status é OK."""
        return self.value == "OK"

    def is_nok(self) -> bool:
        """Verifica se o status é NOK."""
        return self.value == "NOK"
