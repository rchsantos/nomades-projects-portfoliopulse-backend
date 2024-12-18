import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import (
    user,
    auth,
    portfolio,
    asset,
    transaction,
    prediction
)

# Initialize fastapi app
app = FastAPI(
  debug = os.getenv('DEBUG', False),
  title = os.getenv('APP_NAME', 'PortfolioPulse API'),
  description = os.getenv('APP_DESCRIPTION', 'API for PortfolioPulse'),
  version = os.getenv('APP_VERSION', '0.1.0')
)
prefix = "/api/v1"

# Defining the origins for CORS
origins = [os.getenv('FRONTEND_URL')]

# Adding CORS middleware
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

# TODO: Add a route to handle the root URL When the Application is deployed
# Import and include routers from all modules in app.routes dynamically.
# package = 'app.routes'
# for _, module_name, _ in pkgutil.iter_modules([package.replace('.', '/')]):
#   module = importlib.import_module(f'{package}.{module_name}')
#   if hasattr(module, 'router'):
#     app.include_router(getattr(module, 'router'), prefix=prefix)

app.include_router(auth.router, prefix=prefix)
app.include_router(user.router, prefix=prefix)
app.include_router(portfolio.router, prefix=prefix)
app.include_router(asset.router, prefix=prefix)
app.include_router(transaction.router, prefix=prefix)
app.include_router(prediction.router, prefix=prefix)


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=5050, reload=True)
