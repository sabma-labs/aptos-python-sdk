# Copyright © Endless Foundation
# Copyright © Aptos Foundation
# SPDX-License-Identifier: Apache-2.0

import asyncio

from endless_sdk.account_address import AccountAddress
from endless_sdk.async_client import RestClient

from .common import NODE_URL


async def main():
    rest_client = RestClient(NODE_URL)
    total_apt = await rest_client.aggregator_value(
        AccountAddress.from_str("0x1"),
        "0x1::coin::CoinInfo<0x1::endless_coin::EndlessCoin>",
        ["supply"],
    )
    print(f"Total circulating APT: {total_apt}")
    await rest_client.close()


if __name__ == "__main__":
    asyncio.run(main())
