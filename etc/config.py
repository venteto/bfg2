import dataclasses
import os

# only for items in .env rather than .envrc
from dotenv import load_dotenv

load_dotenv()

# to make seeing logger output optional
BFG_ENV = os.environ.get('BFG_ENV', None)

SERVICE_DID = os.environ.get('BFG_SERVICE_DID', None)
HOSTNAME = os.environ.get('BFG_HOSTNAME', None)

if HOSTNAME is None:
    raise RuntimeError('You should set "HOSTNAME" environment variable first.')

if SERVICE_DID is None:
    SERVICE_DID = f'did:web:{HOSTNAME}'


PUB_ERR_MSG = 'Publish your feed first to obtain Feed URI.'

# ------------------------------------------------
# feed URIs
# ------------------------------------------------

ARTISTS_URI = os.environ.get('BFG_URI_ARTISTS')
if ARTISTS_URI is None:
    raise RuntimeError(PUB_ERR_MSG)

MUSEUMS_URI = os.environ.get('BFG_URI_MUSEUMS')
if MUSEUMS_URI is None:
    raise RuntimeError(PUB_ERR_MSG)


# ------------------------------------------------
# for the feed generators publisher script
# ------------------------------------------------

@dataclasses.dataclass
class Feed:
    record_name: str
    display_name: str
    description: str
    emoji: list[str]
    hashtags: list[str]

# Account
HANDLE = os.environ.get('BFG_HANDLE', None)
PASSWORD = os.environ.get('BFG_PASSWORD', None)

BASE_DESCRIPTION: str = '\n\nPowered by the AT Protocol SDK for Python\nhttps://github.com/MarshalX/atproto'

TMP_DESCRIPTION = 'Test feed to compare feed accuracy to a native curated user list'

"""
    record_name = os.environ.get('SOME_SLUG', None)
"""

# ------------------------------------------------

class Artists(Feed):
    record_name = 'artists'
    display_name = '🦋 Artists'
    description = TMP_DESCRIPTION + BASE_DESCRIPTION

class Museums(Feed):
    record_name = 'museums'
    display_name = '🦋 Museums'
    description = TMP_DESCRIPTION + BASE_DESCRIPTION

# ------------------------------------------------

FEEDS = [Artists, Museums]
