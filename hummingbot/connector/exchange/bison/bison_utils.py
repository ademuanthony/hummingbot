from decimal import Decimal
from typing import Any, Dict

from pydantic import Field, SecretStr

from hummingbot.client.config.config_data_types import BaseConnectorConfigMap, ClientFieldData
from hummingbot.connector.exchange.bison.app_data import app_data_dir
from hummingbot.core.data_type.trade_fee import TradeFeeSchema

CENTRALIZED = True
EXAMPLE_PAIR = "ZRX-ETH"

DEFAULT_FEES = TradeFeeSchema(
    maker_percent_fee_decimal=Decimal("0.001"),
    taker_percent_fee_decimal=Decimal("0.001"),
    buy_percent_fee_deducted_from_returns=True
)


def is_exchange_information_valid(exchange_info: Dict[str, Any]) -> bool:
    """
    Verifies if a trading pair is enabled to operate with based on its exchange information
    :param exchange_info: the exchange information for a trading pair
    :return: True if the trading pair is enabled, False otherwise
    """
    is_spot = False
    is_trading = False

    if exchange_info.get("status", None) == "TRADING":
        is_trading = True

    permissions_sets = exchange_info.get("permissionSets", list())
    for permission_set in permissions_sets:
        # PermissionSet is a list, find if in this list we have "SPOT" value or not
        if "SPOT" in permission_set:
            is_spot = True
            break

    return is_trading and is_spot


class BisonConfigMap(BaseConnectorConfigMap):
    connector: str = Field(default="bison", const=True, client_data=None)
    bison_rpc_host: str = Field(
        default="https://127.0.0.1:5757",
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your Bison RPC Host",
            is_secure=False,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )
    bison_rpc_username: str = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your Bison RPC username",
            is_secure=False,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )
    bison_rpc_password: SecretStr = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your Bison RPC password",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )
    bison_cert_path: str = Field(
        default=app_data_dir("dcrx") + "/rpc.cert",
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your Bison certificate path",
            is_secure=False,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )
    bison_app_password: SecretStr = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your Bison app password",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )

    class Config:
        title = "bison"


KEYS = BisonConfigMap.construct()
