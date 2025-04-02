# Copyright © Aptos Foundation
# SPDX-License-Identifier: Apache-2.0

import asyncio
import json
# import sys
# import os

# # Append the path to the directory containing the aptos_sdk folder
# sdk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(sdk_path)

from aptos_sdk.account import Account
from aptos_sdk.aptos_tokenv1_client import AptosTokenV1Client
from aptos_sdk.async_client import FaucetClient, RestClient

from .common import FAUCET_AUTH_TOKEN, FAUCET_URL, NODE_URL

import pdb
async def main():
    rest_client = RestClient(NODE_URL)
    # faucet_client = FaucetClient(FAUCET_URL, rest_client, FAUCET_AUTH_TOKEN)
    token_client = AptosTokenV1Client(rest_client)

    # :!:>section_2
    # alice = Account.generate()
    # bob = Account.generate()  
    # # <:!:section_2
    niraj =  Account.load_key("0x68e7f9a75606e0baa3c2487b32ba016ead6d8d71a220f5a69a8b7645468c54df")
    bob =  Account.load_key("0x7bdbb1a41263b886e8d1fe5f5299874310946e9ef4a2a9317c2c632bcb5641d9")
    collection_name = "niraj_first"
    token_name = "niraj's first token"
    property_version = 0

    # print("\n=== Addresses ===")
    # print(f"Alice: {niraj.address()}")
    # print(f"Bob: {bob.address()}")

    # :!:>section_3
    # bob_fund = faucet_client.fund_account(alice.address(), 100_000_000)
    # alice_fund = faucet_client.fund_account(bob.address(), 100_000_000)  # <:!:section_3
    # await asyncio.gather(*[bob_fund, alice_fund])

    # print("\n=== Initial Coin Balances ===")
    alice_balance = rest_client.account_balance(niraj.address())
    bob_balance = rest_client.account_balance(bob.address())
    [alice_balance, bob_balance] = await asyncio.gather(*[alice_balance, bob_balance])
    # print(f"Alice: {alice_balance}")
    # print(f"Bob: {bob_balance}")

    # print("\n=== Creating Collection and Token ===")
    # :!:>section_4
    # txn_hash = await token_client.create_collection(
    #     niraj,"Alnirajce's simple collection", collection_name, "https://endless.dev"
    # )  # <:!:section_4
    # await rest_client.wait_for_transaction(txn_hash)

    # :!:>section_5
    txn_hash = await token_client.create_token(
        niraj,
        collection_name,
        token_name,
        "Niraj's simple token",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Cat_November_2010-1a.jpg/800px-Cat_November_2010-1a.jpg",
        0,
    )  # <:!:section_5
    
    await rest_client.wait_for_transaction(txn_hash)

    # :!:>section_6
    collection_data = await token_client.get_collection(
        niraj.address(), collection_name
    )
    print(
        f"Alice's collection: {json.dumps(collection_data, indent=4, sort_keys=True)}"
    )  # <:!:section_6
    # :!:>section_7
    balance = await token_client.get_token_balance(
        niraj.address(), niraj.address(), collection_name, token_name, property_version
    )
    print(f"Alice's token balance: {balance}")  # <:!:section_7
    # :!:>section_8
    token_data = await token_client.get_token_data(
        niraj.address(), collection_name, token_name, property_version
    )
    print(
        f"Alice's token data: {json.dumps(token_data, indent=4, sort_keys=True)}"
    )  # <:!:section_8

    print("\n=== Transferring the token to Bob ===")
    # :!:>section_9
    txn_hash = await token_client.offer_token(
        niraj,
        bob.address(),
        niraj.address(),
        collection_name,
        token_name,
        property_version,
        1,
    )  # <:!:section_9
    await rest_client.wait_for_transaction(txn_hash)

    # :!:>section_10
    txn_hash = await token_client.claim_token(
        bob,
        niraj.address(),
        niraj.address(),
        collection_name,
        token_name,
        property_version,
    )  # <:!:section_10
    await rest_client.wait_for_transaction(txn_hash)

    alice_balance = token_client.get_token_balance(
        niraj.address(), niraj.address(), collection_name, token_name, property_version
    )
    bob_balance = token_client.get_token_balance(
        bob.address(), niraj.address(), collection_name, token_name, property_version
    )
    [alice_balance, bob_balance] = await asyncio.gather(*[alice_balance, bob_balance])
    print(f"Alice's token balance: {alice_balance}")
    print(f"Bob's token balance: {bob_balance}")

    print("\n=== Transferring the token back to Alice using MultiAgent ===")
    txn_hash = await token_client.direct_transfer_token(
        bob, niraj , niraj.address(), collection_name, token_name, 0, 1
    )
    await rest_client.wait_for_transaction(txn_hash)

    alice_balance = token_client.get_token_balance(
        niraj.address(), niraj.address(), collection_name, token_name, property_version
    )
    bob_balance = token_client.get_token_balance(
        bob.address(), niraj.address(), collection_name, token_name, property_version
    )
    [alice_balance, bob_balance] = await asyncio.gather(*[alice_balance, bob_balance])
    print(f"Alice's token balance: {alice_balance}")
    print(f"Bob's token balance: {bob_balance}")

    await rest_client.close()


if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
