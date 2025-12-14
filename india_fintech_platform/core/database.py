"""
Database layer for India FinTech Platform
In-memory for demo, would use PostgreSQL in production
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from .models import User, CreditProfile, Transaction, ProductType


class Database:
    """In-memory database for demonstration"""
    
    def __init__(self):
        self._users: Dict[str, User] = {}
        self._credit_profiles: Dict[str, CreditProfile] = {}
        self._transactions: Dict[str, Transaction] = {}
        self._products: Dict[str, Dict[str, Any]] = {}  # product_type -> {id: product}
        self._audit_logs: List[Dict[str, Any]] = []
    
    # User operations
    def create_user(self, user: User) -> User:
        self._users[user.id] = user
        self._log_action("create", "user", user.id)
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)
    
    def get_user_by_phone(self, phone: str) -> Optional[User]:
        for user in self._users.values():
            if user.phone == phone:
                return user
        return None
    
    def update_user(self, user: User) -> User:
        user.updated_at = datetime.now()
        self._users[user.id] = user
        self._log_action("update", "user", user.id)
        return user
    
    def list_users(self, limit: int = 100, offset: int = 0) -> List[User]:
        users = list(self._users.values())
        return users[offset:offset + limit]
    
    # Credit Profile operations
    def create_credit_profile(self, profile: CreditProfile) -> CreditProfile:
        self._credit_profiles[profile.user_id] = profile
        self._log_action("create", "credit_profile", profile.user_id)
        return profile
    
    def get_credit_profile(self, user_id: str) -> Optional[CreditProfile]:
        return self._credit_profiles.get(user_id)
    
    def update_credit_profile(self, profile: CreditProfile) -> CreditProfile:
        profile.last_updated = datetime.now()
        self._credit_profiles[profile.user_id] = profile
        self._log_action("update", "credit_profile", profile.user_id)
        return profile
    
    # Transaction operations
    def create_transaction(self, txn: Transaction) -> Transaction:
        self._transactions[txn.id] = txn
        self._log_action("create", "transaction", txn.id)
        return txn
    
    def get_transaction(self, txn_id: str) -> Optional[Transaction]:
        return self._transactions.get(txn_id)
    
    def get_user_transactions(self, user_id: str, limit: int = 100) -> List[Transaction]:
        user_txns = [t for t in self._transactions.values() if t.user_id == user_id]
        user_txns.sort(key=lambda t: t.created_at, reverse=True)
        return user_txns[:limit]
    
    def update_transaction(self, txn: Transaction) -> Transaction:
        self._transactions[txn.id] = txn
        self._log_action("update", "transaction", txn.id)
        return txn
    
    # Product operations
    def store_product(self, product_type: str, product_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if product_type not in self._products:
            self._products[product_type] = {}
        self._products[product_type][product_id] = data
        self._log_action("create", product_type, product_id)
        return data
    
    def get_product(self, product_type: str, product_id: str) -> Optional[Dict[str, Any]]:
        return self._products.get(product_type, {}).get(product_id)
    
    def get_user_products(self, product_type: str, user_id: str) -> List[Dict[str, Any]]:
        products = self._products.get(product_type, {})
        return [p for p in products.values() if p.get('user_id') == user_id]
    
    def update_product(self, product_type: str, product_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if product_type in self._products and product_id in self._products[product_type]:
            self._products[product_type][product_id].update(data)
            self._log_action("update", product_type, product_id)
        return self._products.get(product_type, {}).get(product_id, {})
    
    # Audit logging
    def _log_action(self, action: str, resource_type: str, resource_id: str):
        self._audit_logs.append({
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'resource_type': resource_type,
            'resource_id': resource_id,
        })
    
    def get_audit_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self._audit_logs[-limit:]
    
    # Statistics
    def get_stats(self) -> Dict[str, Any]:
        return {
            'total_users': len(self._users),
            'credit_profiles': len(self._credit_profiles),
            'transactions': len(self._transactions),
            'products': {k: len(v) for k, v in self._products.items()},
            'audit_logs': len(self._audit_logs),
        }


# Global database instance
db = Database()
