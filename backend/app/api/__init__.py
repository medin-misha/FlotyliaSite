from fastapi import APIRouter

main_router = APIRouter(prefix="/api/v1")

from .v1.users.views import router as users_router
from .v1.contract import router as contract_router
from .v1.transport import router as transport_router
from .v1.admin import router as admin_router
from .v1.files.views import router as files_router
from .v1.document import router as document_router

main_router.include_router(users_router)
main_router.include_router(contract_router)
main_router.include_router(transport_router)
main_router.include_router(admin_router)
main_router.include_router(files_router)
main_router.include_router(document_router)
