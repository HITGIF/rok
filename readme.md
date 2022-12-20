## Usage
1. Create and fill in `config.py` from the template:
```python
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Config:
    ngrok_auth_token: str = "..."
    ngrok_port: int = ...
    discord_guild_id: int = ...
    discord_channel_id: int = ...
    discord_bot_token: str = "..."

    @staticmethod
    def address_handler(address: str) -> str:
        ...
        return "THE NEW ADDRESS"

```
2. Run
```shell
python rok.py [ngrok port] [ngrok protocol]
```