from .base import BaseServerInstaller, InstallResult
from .fabric import FabricServerInstaller
from .forge import ForgeServerInstaller
from .paper import PaperServerInstaller
from .vanilla import VanillaServerInstaller

SERVER_TYPES: dict[str, type[BaseServerInstaller]] = {
    installer.id: installer
    for installer in (
        VanillaServerInstaller,
        FabricServerInstaller,
        ForgeServerInstaller,
        PaperServerInstaller,
    )
}


def get_installer(server_type_id: str) -> BaseServerInstaller:
    installer_cls = SERVER_TYPES.get(server_type_id)
    if installer_cls is None:
        raise ValueError(f"Unknown server type: {server_type_id}")
    return installer_cls()


__all__ = [
    "BaseServerInstaller",
    "InstallResult",
    "SERVER_TYPES",
    "get_installer",
]
