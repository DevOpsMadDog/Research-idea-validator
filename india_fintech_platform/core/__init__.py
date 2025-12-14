"""
India FinTech Platform - Core Module
Building missing financial products for 1.4 billion Indians
"""

from .models import User, CreditProfile, Transaction
from .database import Database
from .config import Config

__all__ = ['User', 'CreditProfile', 'Transaction', 'Database', 'Config']
