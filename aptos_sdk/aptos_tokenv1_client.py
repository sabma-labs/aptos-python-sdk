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
from typing import Optional, List, TypeVar, Generic
from .aptos_token_client import Royalty 
T = TypeVar('T', bound='Serializable')

class Royalty:
    numerator: int
    denominator: int
    payee_address: AccountAddress

    struct_tag: str = "0x4::royalty::Royalty"

    def __init__(self, numerator, denominator, payee_address):
        self.numerator = numerator
        self.denominator = denominator
        self.payee_address = payee_address

    def __str__(self) -> str:
        return f"Royalty[numerator: {self.numerator}, denominator: {self.denominator}, payee_address: {self.payee_address}]"

    @staticmethod
    def parse(resource: dict[str, Any]):
        payee = resource["payee_address"]
        if isinstance(payee, AccountAddress):
            address = payee
        else:
            address = AccountAddress.from_str_relaxed(payee)
        return Royalty(
            resource["numerator"],
            resource["denominator"],
            address,
        )     
    def serialize(self, serializer: Serializer) -> None:
        print("Serializing Royalty")
        serializer.u64(self.numerator)
        serializer.u64(self.denominator)
        serializer.struct(self.payee_address)


class Option:
    """
    A Python implementation of a Move Option type that serializes an optional value as:
      - 0x00 if the value is None,
      - 0x01 followed by the serialized value if present.
    """

    struct_tag: str = "0x1::option::Option"

    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        if self.value is None:
            return "Option[None]"
        else:
            return f"Option[Some: {self.value}]"

    @staticmethod
    def parse(resource: dict[str, Any], inner_parser) -> "Option":
        """
        Parse an Option from a resource dictionary.
        
        Args:
            resource (dict[str, Any]): A dictionary representing the serialized option.
            inner_parser (Callable[[Any], T]): A function that can parse the inner value.
            
        Returns:
            Option[T]: The parsed Option instance.
            
        Note:
            The resource dictionary is expected to have a key "tag" indicating 0 (None) or 1 (Some),
            and if Some, a key "value" containing the serialized inner value.
        """
        tag = resource.get("tag")
        if tag == 0:
            return Option(None)
        elif tag == 1:
            inner_value = inner_parser(resource.get("value"))
            return Option(inner_value)
        else:
            raise Exception("Invalid tag for Option")

    def serialize(self, serializer: "Serializer") -> None:
        if self.value is None:
            serializer.u8(0)  # Write 0x00 for None.
        else:
            serializer.u8(1)  # Write 0x01 for Some.
            self.value.serialize(serializer)

    def bcs_to_bytes(self) -> bytes:
        """
        Serializes this Option instance into BCS bytes.
        """
        serializer = Serializer()
        self.serialize(serializer)
        return serializer.output()

    def serialize_for_entry_function(self, serializer: "Serializer") -> None:
        """
        For entry functions, serialize the Option using a fixed bytes length.
        """
        bcs_bytes = self.bcs_to_bytes()
        serializer.fixed_bytes(bcs_bytes)

    def unwrap(self) -> T:
        if self.value is None:
            raise Exception("Called unwrap on an Option with no value")
        return self.value

    def is_some(self) -> bool:
        return self.value is not None
             
# class Royalty(Serializable):
#     def __init__(self, numerator: int, denominator: int, payee_address: AccountAddress):
#         self.numerator = numerator
#         self.denominator = denominator
#         self.payee_address = payee_address

#     def serialize(self, serializer: Serializer) -> None:
#         print("Serializing Royalty")
#         serializer.u64(self.numerator)
#         serializer.u64(self.denominator)
#         serializer.struct(self.payee_address) 


class AptosTokenV1Client:
    """A wrapper around reading and mutating AptosTokens also known as Token Objects"""

    _client: RestClient

    def __init__(self, client: RestClient):
        self._client = client

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
        uri: str,
        royalty_points_per_million: int,
    ) -> str:
        # Create a Royalty instance
        royalty = Royalty.parse({
            "numerator": royalty_points_per_million,
            "denominator": 1000000,
            "payee_address": str(account.address())
        })
        # royalty = Royalty(royalty_points_per_million, 1000000, account.address())
        royalty_option = Option(royalty)
        serialized_bytes = royalty_option.bcs_to_bytes()
        hex_string = serialized_bytes.hex()
        print("Serialized Royalty Option:", hex_string)
        # pdb.set_trace()
        # x = TransactionArgument([royalty], Serializer.sequence_serializer(Serializer.struct))
        transaction_arguments = [
            TransactionArgument(collection_name, Serializer.str),
            TransactionArgument(name, Serializer.str),
            TransactionArgument(description, Serializer.str),
            TransactionArgument(royalty_option, Serializer.serialize_option),  # Use an option serializer if required
            TransactionArgument(uri, Serializer.str),
        ]
        # transaction_arguments = [
        # TransactionArgument(collection_name, Serializer.str),
        # TransactionArgument(name, Serializer.str),
        # TransactionArgument(description, Serializer.str),
        # TransactionArgument(uri, Serializer.str),
        # ]
        
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
