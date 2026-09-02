from terminalforge.core.config import ConfigStore
from terminalforge.core.models import AccountProfile, Provider

def test_account_roundtrip(tmp_path):
    s = ConfigStore(tmp_path / 'accounts.json')
    s.save_accounts([AccountProfile(provider=Provider.GOOGLE, name='work', group='engineering', model='gemini-2.5-flash', secret_ref='X')])
    a = s.load_accounts()[0]
    assert a.provider == Provider.GOOGLE and a.name == 'work' and a.group == 'engineering'
