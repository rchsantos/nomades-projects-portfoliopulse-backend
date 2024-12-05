from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user, get_transaction_service
from app.schemas.transaction import TransactionResponse, TransactionCreate, TransactionUpdate
from app.schemas.user import UserResponse
from app.services.transaction import TransactionService

router = APIRouter(
  prefix='/portfolio/{portfolio_id}/transaction',
  tags=['transaction']
)

@router.get(
  '/',
  response_model=list[TransactionResponse],
  status_code=status.HTTP_200_OK,
  description='Get all transactions for a portfolio',
  response_description='Transactions retrieved successfully'
)
async def get_all_transactions(
  portfolio_id: str,
  transaction_service: TransactionService = Depends(get_transaction_service),
  current_user: UserResponse = Depends(get_current_user)
):
  try:
    user = await current_user
    return await transaction_service.fetch_all_transactions(portfolio_id, user.id)
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))

@router.post(
  '/',
  response_model=TransactionResponse,
  status_code=status.HTTP_201_CREATED,
  description='Create a new transaction for an asset',
  response_description='Transaction created successfully'
)
async def create_transaction(
  portfolio_id: str,
  transaction_data: TransactionCreate,
  transaction_service: TransactionService = Depends(get_transaction_service),
  current_user: UserResponse = Depends(get_current_user)
):
  try:
    user = await current_user
    return await transaction_service.create_transaction(portfolio_id, user.id, transaction_data)
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))

@router.patch(
  '/{transaction_id}',
  response_model=TransactionResponse,
  status_code=status.HTTP_200_OK,
  description='Update a transaction',
  response_description='Transaction updated successfully'
)
async def update_transaction(
  portfolio_id: str,
  transaction_id: str,
  transaction: TransactionUpdate,
  transaction_service: TransactionService = Depends(get_transaction_service),
  current_user: UserResponse = Depends(get_current_user)
):
  try:
    user = await current_user
    return await transaction_service.update_transaction(portfolio_id, user.id, transaction_id, transaction)
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))

@router.delete(
    '/{transaction_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    description='Delete a transaction',
    response_description='Transaction deleted successfully'
)
async def delete_transaction(
    portfolio_id: str,
    transaction_id: str,
    transaction_service: TransactionService = Depends(get_transaction_service),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        user = await current_user
        await transaction_service.delete_transaction(portfolio_id, user.id, transaction_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
