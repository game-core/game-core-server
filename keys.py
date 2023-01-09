from gc_integrations.config import load_env_secrets, GCISecrets
from gc_integrations.igdb.models.auth_models import IGDBAuth

gci_secrets: GCISecrets = load_env_secrets()
gc_secrets = None
