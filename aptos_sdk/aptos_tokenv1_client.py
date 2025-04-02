# Copyright © Aptos Foundation
# SPDX-License-Identifier: Apache-2.0

from typing import Any, Optional
import pdb
from .account import Account
from .account_address import AccountAddress
from .async_client import ApiError, RestClient
from .bcs import Serializer
from .transactions import EntryFunction, TransactionArgument, TransactionPayload

U64_MAX = 100
from aptos_sdk.bcs import Serializable, Serializer
class Royalty:
    def __init__(self, numerator: int, denominator: int, payee_address: AccountAddress):
        self.numerator = numerator
        self.denominator = denominator
        self.payee_address = payee_address

    def serialize(self, serializer: Serializer) -> None:
        print("Serializing Royalty")
        serializer.u64(self.numerator)
        serializer.u64(self.denominator)
        serializer.struct(self.payee_address)

import io

class RoyaltyOption:
    def __init__(self, value: Optional[Royalty] = None):
        # Internally, we use a list to represent a MoveVector-like structure.
        self.vec = [value] if value is not None else []
        self.value = self.vec[0] if self.vec else None

    def serialize_for_entry_function(self, serializer: Serializer) -> None:
        """
        Serializes the RoyaltyOption for use in an entry function.
        This method converts the object to BCS bytes and writes them using the serializer.
        """
        bcs_bytes = self.bcs_to_bytes()
        serializer.fixed_bytes(bcs_bytes)

    def bcs_to_bytes(self) -> bytes:
        """
        Serializes the current instance using BCS (Binary Canonical Serialization).
        This helper method writes the serialized bytes into a BytesIO stream.
        """
        stream = io.BytesIO()
        temp_serializer = Serializer(stream)
        self.serialize(temp_serializer)
        return stream.getvalue()

    def serialize(self, serializer: Serializer) -> None:
        """
        Serializes the RoyaltyOption.
        If a value is present, writes a flag of 1 followed by the Royalty's serialization.
        Otherwise, writes a flag of 0.
        """
        if self.is_some():
            print("Serializing RoyaltyOption: Some")
            serializer.u8(1)
            self.value.serialize(serializer)
        else:
            print("Serializing RoyaltyOption: None")
            serializer.u8(0)

    def unwrap(self) -> Royalty:
        """
        Retrieves the inner Royalty value.
        Raises:
            ValueError: If no value is present.
        Returns:
            The contained Royalty instance.
        """
        if not self.is_some():
            raise ValueError("Called unwrap on a RoyaltyOption with no value")
        return self.vec[0]

    def is_some(self) -> bool:
        """
        Checks if the RoyaltyOption contains a value.
        Returns:
            True if a value is present, False otherwise.
        """
        return len(self.vec) == 1
    
# def option_serializer(serializer: Serializer, option: Option):
#     option.serialize(serializer)



# class Option(Serializable):
#     def __init__(self, value=None):
#         self.value = value

#     def serialize(self, serializer: Serializer) -> None:
#         if self.value is None:
#             print("Serializing Option: None")
#             serializer.u8(0)
#         else:
#             print("Serializing Option: Some")
#             serializer.u8(1)
#             self.value.serialize(serializer)


#     @classmethod
#     def some(cls, value):
#         return cls(value)

#     @classmethod
#     def none(cls):
#         return cls(None)

# def option_serializer(serializer: Serializer, option: Option):
#     option.serialize(serializer)

# class Royalty(Serializable):
#     def __init__(self, numerator: int, denominator: int, payee_address: AccountAddress):
#         self.numerator = numerator
#         self.denominator = denominator
#         self.payee_address = payee_address

#     def serialize(self, serializer: Serializer) -> None:
#         print("applyyyyyyyyyyyyyyyyyyyyyyyyyy")
#         serializer.u64(self.numerator)
#         serializer.u64(self.denominator)
#         serializer.struct(self.payee_address)

class AptosTokenV1Client:
    """A wrapper around reading and mutating AptosTokens also known as Token Objects"""

    _client: RestClient

    def __init__(self, client: RestClient):
        self._client = client

    # async def create_collection(
    #     self, account: Account, name: str, description: str, uri: str
    # ) -> str:
    #     """Creates a new collection within the specified account"""

    #     transaction_arguments = [
    #         TransactionArgument(name, Serializer.str),
    #         TransactionArgument(description, Serializer.str),
    #         TransactionArgument(uri, Serializer.str),
    #         TransactionArgument(U64_MAX, Serializer.u64),
    #         TransactionArgument(
    #             [False, False, False], Serializer.sequence_serializer(Serializer.bool)
    #         ),
    #     ]

    #     payload = EntryFunction.natural(
    #         "0x4::nft",
    #         "create_collection",
    #         [],
    #         transaction_arguments,
    #     )

    #     signed_transaction = await self._client.create_bcs_signed_transaction(
    #         account, TransactionPayload(payload)
    #     )
    #     return await self._client.submit_bcs_transaction(signed_transaction)

    async def  create_collection(
    self,
    account: Account,
    description: str,
    name: str,
    uri: str,
    mutable_description: bool = True,
    mutable_royalty: bool = True,
    mutable_uri: bool = True,
    mutable_token_description: bool = True,
    mutable_token_name: bool = True,
    mutable_token_properties: bool = True,
    mutable_token_uri: bool = True,
    tokens_burnable_by_creator: bool = False,
    tokens_freezable_by_creator: bool = False,
    royalty_numerator: int = 0,
    royalty_denominator: int = 1,
    ) -> str:
        """
        Creates a new collection on-chain.
        The Move function signature (excluding the signer) is:
        (description: string, max_supply: u64, name: string, uri: string,
        mutable_description: bool, mutable_royalty: bool, mutable_uri: bool,
        mutable_token_description: bool, mutable_token_name: bool,
        mutable_token_properties: bool, mutable_token_uri: bool,
        tokens_burnable_by_creator: bool, tokens_freezable_by_creator: bool,
        royalty_numerator: u64, royalty_denominator: u64)
        """

        transaction_arguments = [
            
            TransactionArgument(description, Serializer.str),
            TransactionArgument(U64_MAX, Serializer.u64),
            TransactionArgument(name, Serializer.str),
            TransactionArgument(uri, Serializer.str),
            TransactionArgument(mutable_description, Serializer.bool),
            TransactionArgument(mutable_royalty, Serializer.bool),
            TransactionArgument(mutable_uri, Serializer.bool),
            TransactionArgument(mutable_token_description, Serializer.bool),
            TransactionArgument(mutable_token_name, Serializer.bool),
            TransactionArgument(mutable_token_properties, Serializer.bool),
            TransactionArgument(mutable_token_uri, Serializer.bool),
            TransactionArgument(tokens_burnable_by_creator, Serializer.bool),
            TransactionArgument(tokens_freezable_by_creator, Serializer.bool),
            TransactionArgument(royalty_numerator, Serializer.u64),
            TransactionArgument(royalty_denominator, Serializer.u64),
        ]
        # pdb.set_trace()
        payload = EntryFunction.natural(
            "0x4::nft", "create_collection", [], transaction_arguments
        )

        signed_transaction = await self._client.create_bcs_signed_transaction(
            account, TransactionPayload(payload)
        )
        
        return await self._client.submit_bcs_transaction(signed_transaction)

    
    async def create_token(
        self,
        account: Account,
        collection_name: str,
        name: str,
        description: str,
        supply: int,
        uri: str,
        royalty_points_per_million: int,
    ) -> str:
        # Create a Royalty instance
        print(f"Acoount address type: {type(account.address())}")
        royalty = Royalty(royalty_points_per_million, 1000000, account.address())

        # Wrap it in an Option (using Option.some)
        royalty_option = RoyaltyOption(royalty)

        # transaction_arguments = [
        #     TransactionArgument(collection_name, Serializer.str),
        #     TransactionArgument(description, Serializer.str),
        #     TransactionArgument(name, Serializer.str),
        #     TransactionArgument(royalty_option, Serializer.struct),  # Use an option serializer if required
        #     TransactionArgument(uri, Serializer.str),
        # ]
        transaction_arguments = [
        TransactionArgument(collection_name, Serializer.str),
        TransactionArgument(description, Serializer.str),
        TransactionArgument(name, Serializer.str),
        TransactionArgument(royalty_option, royalty_option.serialize_for_entry_function(Serializer)),
        TransactionArgument(uri, Serializer.str),
        ]

        payload = EntryFunction.natural(
            "0x4::token",
            "create_named_token",
            [],
            transaction_arguments,
        )
        signed_transaction = await self._client.create_bcs_signed_transaction(
            account, TransactionPayload(payload)
        )
        return await self._client.submit_bcs_transaction(signed_transaction)

    async def offer_token(
        self,
        account: Account,
        receiver: AccountAddress,
        creator: AccountAddress,
        collection_name: str,
        token_name: str,
        property_version: int,
        amount: int,
    ) -> str:
        transaction_arguments = [
            TransactionArgument(receiver, Serializer.struct),
            TransactionArgument(creator, Serializer.struct),
            TransactionArgument(collection_name, Serializer.str),
            TransactionArgument(token_name, Serializer.str),
            TransactionArgument(property_version, Serializer.u64),
            TransactionArgument(amount, Serializer.u64),
        ]

        payload = EntryFunction.natural(
            "0x3::token_transfers",
            "offer_script",
            [],
            transaction_arguments,
        )
        signed_transaction = await self._client.create_bcs_signed_transaction(
            account, TransactionPayload(payload)
        )
        return await self._client.submit_bcs_transaction(signed_transaction)

    async def claim_token(
        self,
        account: Account,
        sender: AccountAddress,
        creator: AccountAddress,
        collection_name: str,
        token_name: str,
        property_version: int,
    ) -> str:
        transaction_arguments = [
            TransactionArgument(sender, Serializer.struct),
            TransactionArgument(creator, Serializer.struct),
            TransactionArgument(collection_name, Serializer.str),
            TransactionArgument(token_name, Serializer.str),
            TransactionArgument(property_version, Serializer.u64),
        ]

        payload = EntryFunction.natural(
            "0x3::token_transfers",
            "claim_script",
            [],
            transaction_arguments,
        )
        signed_transaction = await self._client.create_bcs_signed_transaction(
            account, TransactionPayload(payload)
        )
        return await self._client.submit_bcs_transaction(signed_transaction)

    async def direct_transfer_token(
        self,
        sender: Account,
        receiver: Account,
        creators_address: AccountAddress,
        collection_name: str,
        token_name: str,
        property_version: int,
        amount: int,
    ) -> str:
        transaction_arguments = [
            TransactionArgument(creators_address, Serializer.struct),
            TransactionArgument(collection_name, Serializer.str),
            TransactionArgument(token_name, Serializer.str),
            TransactionArgument(property_version, Serializer.u64),
            TransactionArgument(amount, Serializer.u64),
        ]

        payload = EntryFunction.natural(
            "0x3::token",
            "direct_transfer_script",
            [],
            transaction_arguments,
        )

        signed_transaction = await self._client.create_multi_agent_bcs_transaction(
            sender,
            [receiver],
            TransactionPayload(payload),
        )
        return await self._client.submit_bcs_transaction(signed_transaction)

    #
    # Token accessors
    #

    async def get_token(
        self,
        owner: AccountAddress,
        creator: AccountAddress,
        collection_name: str,
        token_name: str,
        property_version: int,
    ) -> Any:
        resource = await self._client.account_resource(owner, "0x3::token::TokenStore")
        token_store_handle = resource["data"]["tokens"]["handle"]

        token_id = {
            "token_data_id": {
                "creator": str(creator),
                "collection": collection_name,
                "name": token_name,
            },
            "property_version": str(property_version),
        }

        try:
            return await self._client.get_table_item(
                token_store_handle,
                "0x3::token::TokenId",
                "0x3::token::Token",
                token_id,
            )
        except ApiError as e:
            if e.status_code == 404:
                return {
                    "id": token_id,
                    "amount": "0",
                }
            raise

    async def get_token_balance(
        self,
        owner: AccountAddress,
        creator: AccountAddress,
        collection_name: str,
        token_name: str,
        property_version: int,
    ) -> str:
        info = await self.get_token(
            owner, creator, collection_name, token_name, property_version
        )
        return info["amount"]

    async def get_token_data(
        self,
        creator: AccountAddress,
        collection_name: str,
        token_name: str,
        property_version: int,
    ) -> Any:
        resource = await self._client.account_resource(
            creator, "0x3::token::Collections"
        )
        token_data_handle = resource["data"]["token_data"]["handle"]

        token_data_id = {
            "creator": str(creator),
            "collection": collection_name,
            "name": token_name,
        }

        return await self._client.get_table_item(
            token_data_handle,
            "0x3::token::TokenDataId",
            "0x3::token::TokenData",
            token_data_id,
        )  # <:!:read_token_data_table

    async def get_collection(
        self, creator: AccountAddress, collection_name: str
    ) -> Any:
        resource = await self._client.account_resource(
            creator, "0x3::token::Collections"
        )
        token_data = resource["data"]["collection_data"]["handle"]

        return await self._client.get_table_item(
            token_data,
            "0x1::string::String",
            "0x3::token::CollectionData",
            collection_name,
        )

    async def transfer_object(
        self, owner: Account, object: AccountAddress, to: AccountAddress
    ) -> str:
        transaction_arguments = [
            TransactionArgument(object, Serializer.struct),
            TransactionArgument(to, Serializer.struct),
        ]

        payload = EntryFunction.natural(
            "0x1::object",
            "transfer_call",
            [],
            transaction_arguments,
        )

        signed_transaction = await self._client.create_bcs_signed_transaction(
            owner,
            TransactionPayload(payload),
        )
        return await self._client.submit_bcs_transaction(signed_transaction)
