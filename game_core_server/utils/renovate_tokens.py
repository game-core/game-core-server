import asyncio
from gc_integrations.igdb.models.auth_models import IGDBAuth
from gc_integrations.igdb.utils import get_igdb_auth_token
from keys import gci_secrets

igdb_auth: IGDBAuth | None = None


async def renovate_igdb_token() -> IGDBAuth:
    return await get_igdb_auth_token(
        gci_secrets.IGDB_CLIENT_ID, gci_secrets.IGDB_CLIENT_SECRET
    )


async def get_current_igdb_token() -> IGDBAuth:
    # 30 minutes in miliseconds
    min_viable_time = 30 * 600000
    global igdb_auth

    if igdb_auth is None or igdb_auth.expires_in is None:
        igdb_auth = await renovate_igdb_token()

    else:
        try:
            exp_time_int = int(igdb_auth.expires_in)
        except (ValueError, TypeError):
            igdb_auth = await renovate_igdb_token()
            return igdb_auth

        if exp_time_int < min_viable_time:
            igdb = await renovate_igdb_token()

    return igdb_auth
