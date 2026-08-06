from __future__ import annotations

from dataclasses import dataclass, field


class RepoPatcherError(Exception):
    """Error esperado y presentable al usuario."""


class ManifestError(RepoPatcherError):
    """El manifiesto del paquete es inválido."""


class CompatibilityError(RepoPatcherError):
    """La repo no cumple las condiciones del paquete."""


class PatchConflictError(RepoPatcherError):
    """Una operación no encuentra el contexto esperado."""


class CommandError(RepoPatcherError):
    """Un generador o validador terminó con error."""

    def __init__(
        self,
        *,
        kind: str,
        name: str,
        argv: list[str],
        returncode: int,
        stdout: str,
        stderr: str,
    ) -> None:
        self.kind = kind
        self.name = name
        self.argv = tuple(argv)
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        super().__init__(self._format())

    def _format(self) -> str:
        lines = [
            f"Falló el {self.kind} «{self.name}».",
            f"Comando: {' '.join(self.argv)}",
            f"Código de salida: {self.returncode}",
            "",
            "STDOUT:",
            self.stdout.rstrip() or "(vacío)",
            "",
            "STDERR:",
            self.stderr.rstrip() or "(vacío)",
        ]
        return "\n".join(lines)


@dataclass(frozen=True)
class RollbackStep:
    name: str
    success: bool
    detail: str = ""
    uncertain_paths: tuple[str, ...] = ()


@dataclass
class RollbackReport:
    steps: list[RollbackStep] = field(default_factory=list)

    @property
    def complete(self) -> bool:
        return all(step.success for step in self.steps)

    @property
    def uncertain_paths(self) -> list[str]:
        return sorted({path for step in self.steps for path in step.uncertain_paths})

    def add_success(self, name: str, detail: str = "") -> None:
        self.steps.append(RollbackStep(name=name, success=True, detail=detail))

    def add_failure(self, name: str, detail: str, paths: list[str] | tuple[str, ...] = ()) -> None:
        self.steps.append(
            RollbackStep(name=name, success=False, detail=detail, uncertain_paths=tuple(paths))
        )


class ApplyRollbackError(RepoPatcherError):
    """La aplicación falló; conserva el error primario y el resultado del rollback."""

    def __init__(self, primary: BaseException, rollback: RollbackReport) -> None:
        self.primary = primary
        self.rollback = rollback
        super().__init__(self._format())

    def _format(self) -> str:
        lines = ["ERROR DE APLICACIÓN", "", str(self.primary).rstrip(), "", "ROLLBACK", ""]
        for step in self.rollback.steps:
            state = "correcta" if step.success else "FALLÓ"
            lines.append(f"  {step.name}: {state}")
            if step.detail:
                for detail_line in step.detail.rstrip().splitlines():
                    lines.append(f"    {detail_line}")
            if step.uncertain_paths:
                lines.append("    Rutas en estado incierto:")
                lines.extend(f"      {path}" for path in step.uncertain_paths)
        lines.append("")
        if self.rollback.complete:
            lines.append("El rollback se completó correctamente.")
        else:
            lines.append("El rollback quedó incompleto.")
            if self.rollback.uncertain_paths:
                lines.append("Revisa manualmente estas rutas:")
                lines.extend(f"  {path}" for path in self.rollback.uncertain_paths)
            lines.append(
                "Los errores de rollback son secundarios; la causa original de la aplicación "
                "es la indicada al principio."
            )
        return "\n".join(lines)
