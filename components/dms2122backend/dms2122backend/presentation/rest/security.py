""" REST API controllers responsible of handling the security schemas.
"""

from typing import Dict, Optional
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer
from connexion.exceptions import Unauthorized  # type: ignore
from dms2122backend.data.config import BackendConfiguration


def verify_api_key(token: str) -> Dict:
    """Callback testing the received API key.

    Args:
        - token (str): The received API key.

    Raises:
        - Unauthorized: When the given API key is not valid.

    Returns:
        - Dict: Information retrieved from the key to be passed to the endpoints.
    """
    with current_app.app_context():
        cfg: BackendConfiguration = current_app.cfg
        if not token in cfg.get_authorized_api_keys():
            raise Unauthorized('Invalid API key')
    return {}