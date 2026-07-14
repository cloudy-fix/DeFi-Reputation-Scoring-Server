from datetime import datetime
from typing import List, Dict, Any, Optional

from pydantic import BaseModel, Field, condecimal

# Defines the structure of a single transaction
class Transaction(BaseModel):
    document_id: str
    action: str
    timestamp: int
    caller: str
    protocol: str
    poolId: Optional[str] = None
    poolName: Optional[str] = None
    tokenIn: Optional[Dict[str, Any]] = None
    tokenOut: Optional[Dict[str, Any]] = None
    token_address: Optional[str] = None
    amount: Optional[condecimal(max_digits=38, decimal_places=18)] = None
    block_number: Optional[int] = None

# Defines the structure for a protocol's data (e.g., 'dexes')
class ProtocolData(BaseModel):
    protocolType: str
    transactions: List[Transaction]

# Defines the structure of the incoming Kafka message
class WalletTransactionMessage(BaseModel):
    wallet_address: str
    data: List[ProtocolData]

# Defines the structure of the AI score features
class AIFeatures(BaseModel):
    active_days: int
    lp_score: float
    swap_score: float
    total_transaction_count: int
    user_tags: List[str]

# Defines the structure of a category score in the final output
class CategoryScore(BaseModel):
    category: str
    score: float
    transaction_count: int
    features: AIFeatures

# Defines the structure of the final successful Kafka output message
class WalletScoreSuccess(BaseModel):
    wallet_address: str
    zscore: str = Field(..., description="18 decimal places for blockchain compatibility")
    timestamp: int
    categories: List[CategoryScore]

# Defines the structure of the final failed Kafka output message
class WalletScoreFailure(BaseModel):
    wallet_address: str
    timestamp: int
    error: str
