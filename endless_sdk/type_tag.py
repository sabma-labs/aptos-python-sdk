# Copyright © Endless Foundation
# Copyright © Aptos Foundation
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing
import unittest
from typing import List, Tuple

from .account_address import AccountAddress
from .bcs import Deserializable, Deserializer, Serializable, Serializer


class TypeTag(Deserializable, Serializable):
    """TypeTag represents a primitive in Move."""

    BOOL: int = 0
    U8: int = 1
    U64: int = 2
    U128: int = 3
    ACCOUNT_ADDRESS: int = 4
    SIGNER: int = 5
    VECTOR: int = 6
    STRUCT: int = 7
    U16: int = 8
    U32: int = 9
    U256: int = 10

    value: typing.Any

    def __init__(self, value: typing.Any):
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TypeTag):
            return NotImplemented
        return (
            self.value.variant() == other.value.variant() and self.value == other.value
        )

    def __str__(self):
        return self.value.__str__()

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def deserialize(deserializer: Deserializer) -> TypeTag:
        variant = deserializer.uleb128()
        if variant == TypeTag.BOOL:
            return TypeTag(BoolTag.deserialize(deserializer))
        elif variant == TypeTag.U8:
            return TypeTag(U8Tag.deserialize(deserializer))
        elif variant == TypeTag.U16:
            return TypeTag(U16Tag.deserialize(deserializer))
        elif variant == TypeTag.U32:
            return TypeTag(U32Tag.deserialize(deserializer))
        elif variant == TypeTag.U64:
            return TypeTag(U64Tag.deserialize(deserializer))
        elif variant == TypeTag.U128:
            return TypeTag(U128Tag.deserialize(deserializer))
        elif variant == TypeTag.U256:
            return TypeTag(U256Tag.deserialize(deserializer))
        elif variant == TypeTag.ACCOUNT_ADDRESS:
            return TypeTag(AccountAddressTag.deserialize(deserializer))
        elif variant == TypeTag.SIGNER:
            raise NotImplementedError
        elif variant == TypeTag.VECTOR:
            raise NotImplementedError
        elif variant == TypeTag.STRUCT:
            return TypeTag(StructTag.deserialize(deserializer))
        raise NotImplementedError

    def serialize(self, serializer: Serializer):
        serializer.uleb128(self.value.variant())
        serializer.struct(self.value)


class BoolTag(Deserializable, Serializable):
    value: bool

    def __init__(self, value: bool):
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BoolTag):
            return NotImplemented
        return self.value == other.value

    def __str__(self):
        return self.value.__str__()

    def variant(self):
        return TypeTag.BOOL

    @staticmethod
    def deserialize(deserializer: Deserializer) -> BoolTag:
        return BoolTag(deserializer.bool())

    def serialize(self, serializer: Serializer):
        serializer.bool(self.value)


class U8Tag(Deserializable, Serializable):
    value: int

    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, U8Tag):
            return NotImplemented
        return self.value == other.value

    def __str__(self):
        return self.value.__str__()

    def variant(self):
        return TypeTag.U8

    @staticmethod
    def deserialize(deserializer: Deserializer) -> U8Tag:
        return U8Tag(deserializer.u8())

    def serialize(self, serializer: Serializer):
        serializer.u8(self.value)


class U16Tag(Deserializable, Serializable):
    value: int

    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, U16Tag):
            return NotImplemented
        return self.value == other.value

    def __str__(self):
        return self.value.__str__()

    def variant(self):
        return TypeTag.U16

    @staticmethod
    def deserialize(deserializer: Deserializer) -> U16Tag:
        return U16Tag(deserializer.u16())

    def serialize(self, serializer: Serializer):
        serializer.u16(self.value)


class U32Tag(Deserializable, Serializable):
    value: int

    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, U32Tag):
            return NotImplemented
        return self.value == other.value

    def __str__(self):
        return self.value.__str__()

    def variant(self):
        return TypeTag.U32

    @staticmethod
    def deserialize(deserializer: Deserializer) -> U32Tag:
        return U32Tag(deserializer.u32())

    def serialize(self, serializer: Serializer):
        serializer.u32(self.value)


class U64Tag(Deserializable, Serializable):
    value: int

    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, U64Tag):
            return NotImplemented
        return self.value == other.value

    def __str__(self):
        return self.value.__str__()

    def variant(self):
        return TypeTag.U64

    @staticmethod
    def deserialize(deserializer: Deserializer) -> U64Tag:
        return U64Tag(deserializer.u64())

    def serialize(self, serializer: Serializer):
        serializer.u64(self.value)


class U128Tag(Deserializable, Serializable):
    value: int

    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, U128Tag):
            return NotImplemented
        return self.value == other.value

    def __str__(self):
        return self.value.__str__()

    def variant(self):
        return TypeTag.U128

    @staticmethod
    def deserialize(deserializer: Deserializer) -> U128Tag:
        return U128Tag(deserializer.u128())

    def serialize(self, serializer: Serializer):
        serializer.u128(self.value)


class U256Tag(Deserializable, Serializable):
    value: int

    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, U256Tag):
            return NotImplemented
        return self.value == other.value

    def __str__(self):
        return self.value.__str__()

    def variant(self):
        return TypeTag.U256

    @staticmethod
    def deserialize(deserializer: Deserializer) -> U256Tag:
        return U256Tag(deserializer.u256())

    def serialize(self, serializer: Serializer):
        serializer.u256(self.value)


class AccountAddressTag(Deserializable, Serializable):
    value: AccountAddress

    def __init__(self, value: AccountAddress):
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AccountAddressTag):
            return NotImplemented
        return self.value == other.value

    def __str__(self):
        return self.value.__str__()

    def variant(self):
        return TypeTag.ACCOUNT_ADDRESS

    @staticmethod
    def deserialize(deserializer: Deserializer) -> AccountAddressTag:
        return AccountAddressTag(deserializer.struct(AccountAddress))

    def serialize(self, serializer: Serializer):
        serializer.struct(self.value)


class StructTag(Deserializable, Serializable):
    address: AccountAddress
    module: str
    name: str
    type_args: List[TypeTag]

    def __init__(self, address, module, name, type_args):
        self.address = address
        self.module = module
        self.name = name
        self.type_args = type_args

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StructTag):
            return NotImplemented
        return (
            self.address == other.address
            and self.module == other.module
            and self.name == other.name
            and self.type_args == other.type_args
        )

    def __str__(self) -> str:
        value = f"{self.address}::{self.module}::{self.name}"
        if len(self.type_args) > 0:
            value += f"<{self.type_args[0]}"
            for type_arg in self.type_args[1:]:
                value += f", {type_arg}"
            value += ">"
        return value

    @staticmethod
    def from_str(type_tag: str) -> StructTag:
        return StructTag._from_str_internal(type_tag, 0)[0][0].value

    @staticmethod
    def _from_str_internal(type_tag: str, index: int) -> Tuple[List[TypeTag], int]:
        name = ""
        tags = []
        inner_tags: List[TypeTag] = []

        while index < len(type_tag):
            letter = type_tag[index]
            index += 1

            if letter == " ":
                continue

            if letter == "<":
                (inner_tags, index) = StructTag._from_str_internal(type_tag, index)
            elif letter == ",":
                split = name.split("::")
                tag = TypeTag(
                    StructTag(
                        AccountAddress.from_str_relaxed(split[0]),
                        split[1],
                        split[2],
                        inner_tags,
                    )
                )
                tags.append(tag)
                name = ""
                inner_tags = []
            elif letter == ">":
                break
            else:
                name += letter

        split = name.split("::")
        tag = TypeTag(
            StructTag(
                AccountAddress.from_str_relaxed(split[0]),
                split[1],
                split[2],
                inner_tags,
            )
        )
        tags.append(tag)
        return (tags, index)

    def variant(self):
        return TypeTag.STRUCT

    @staticmethod
    def deserialize(deserializer: Deserializer) -> StructTag:
        address = deserializer.struct(AccountAddress)
        module = deserializer.str()
        name = deserializer.str()
        type_args = deserializer.sequence(TypeTag.deserialize)
        return StructTag(address, module, name, type_args)

    def serialize(self, serializer: Serializer):
        self.address.serialize(serializer)
        serializer.str(self.module)
        serializer.str(self.name)
        serializer.sequence(self.type_args, Serializer.struct)


class Test(unittest.TestCase):
    def test_nested_structs(self):
        l0 = "0x0::l0::L0"
        l10 = "0x1::l10::L10"
        l20 = "0x2::l20::L20"
        l11 = "0x1::l11::L11"
        composite = f"{l0}<{l10}<{l20}>, {l11}>"
        derived = StructTag.from_str(composite)
        self.assertEqual(composite, f"{derived}")
        in_bytes = derived.to_bytes()
        from_bytes = StructTag.from_bytes(in_bytes)
        self.assertEqual(derived, from_bytes)


if __name__ == "__main__":
    unittest.main()
