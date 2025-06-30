#!/usr/bin/env python3
"""
Module for password encryption and validation.

This module provides secure password hashing and validation
functionality using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password with a random salt using bcrypt.

    Args:
        password: Plain text password to hash

    Returns:
        Salted and hashed password as bytes
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate a password against its hash.

    Args:
        hashed_password: Previously hashed password as bytes
        password: Plain text password to validate

    Returns:
        True if password matches the hash, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
