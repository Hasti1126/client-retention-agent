"""
Database Connection and Operations
"""

import logging
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

class DatabaseService:
    """
    Database service for client data
    
    For hackathon demo: Uses in-memory mock data
    For production: Would use PostgreSQL with SQLAlchemy
    """
    
    def __init__(self):
        """Initialize database connection"""
        self.clients = []
        self._initialized = False
    
    async def init_db(self):
        """Initialize database with mock data"""
        if self._initialized:
            return
        
        logger.info("Initializing database with mock data...")
        self.clients = self._generate_mock_clients()
        self._initialized = True
        logger.info(f"Database initialized with {len(self.clients)} clients")
    
    def _generate_mock_clients(self) -> List[Dict]:
        """Generate realistic mock client data"""
        
        industries = ['Healthcare', 'Finance', 'Retail', 'Technology', 
                      'Legal', 'Manufacturing', 'Education', 'Real Estate']
        
        clients = []
        
        for i in range(1, 51):  # 50 mock clients
            # Determine if client is at risk (20%)
            is_at_risk = random.random() < 0.2
            
            if is_at_risk:
                # At-risk client characteristics
                client = {
                    'id': i,
                    'name': f"Client {chr(64+i) if i<=26 else i}",
                    'industry': random.choice(industries),
                    'contract_value': random.randint(3000, 12000),
                    'client_since': (datetime.now() - timedelta(days=random.randint(180, 1500))).strftime('%Y-%m-%d'),
                    'payment_delay': random.randint(10, 30),
                    'satisfaction': round(random.uniform(1.5, 3.5), 1),
                    'utilization': round(random.uniform(0.2, 0.55), 2),
                    'sentiment': round(random.uniform(-0.8, -0.1), 2),
                    'tickets': random.randint(20, 45),
                    'last_contact': f"{random.randint(10, 30)} days ago",
                    'communications': []
                }
            else:
                # Healthy client characteristics
                client = {
                    'id': i,
                    'name': f"Client {chr(64+i) if i<=26 else i}",
                    'industry': random.choice(industries),
                    'contract_value': random.randint(4000, 15000),
                    'client_since': (datetime.now() - timedelta(days=random.randint(180, 1500))).strftime('%Y-%m-%d'),
                    'payment_delay': random.randint(0, 5),
                    'satisfaction': round(random.uniform(3.8, 5.0), 1),
                    'utilization': round(random.uniform(0.7, 0.95), 2),
                    'sentiment': round(random.uniform(0.2, 0.9), 2),
                    'tickets': random.randint(5, 15),
                    'last_contact': f"{random.randint(1, 7)} days ago",
                    'communications': []
                }
            
            clients.append(client)
        
        return clients
    
    async def get_all_clients(self) -> List[Dict]:
        """Get all clients"""
        if not self._initialized:
            await self.init_db()
        return self.clients
    
    async def get_client(self, client_id: int) -> Optional[Dict]:
        """Get specific client by ID"""
        if not self._initialized:
            await self.init_db()
        
        for client in self.clients:
            if client['id'] == client_id:
                return client
        return None
    
    async def get_clients_by_risk(self, risk_level: str) -> List[Dict]:
        """Get clients filtered by risk level"""
        # This would need health scores calculated first
        # Simplified for demo
        return await self.get_all_clients()
    
    async def update_client(self, client_id: int, data: Dict) -> Optional[Dict]:
        """Update client data"""
        if not self._initialized:
            await self.init_db()
        
        for i, client in enumerate(self.clients):
            if client['id'] == client_id:
                self.clients[i].update(data)
                return self.clients[i]
        return None


# Global database instance
_db = None

async def get_db() -> DatabaseService:
    """Get database instance"""
    global _db
    if _db is None:
        _db = DatabaseService()
        await _db.init_db()
    return _db

async def init_db():
    """Initialize database"""
    db = await get_db()
    await db.init_db()
    logger.info("Database initialized")