import os
import uvicorn
import importlib
import pkgutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import user, auth, portfolio, asset

# Initialize fastapi app
app = FastAPI(
  debug = True,
  title = 'PortfolioPulse Demo API',
  description = 'This is a demo API for PortfolioPulse',
  version = '0.1.0'
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

# Import and include routers from all modules in app.routes dynamically.
package = 'app.routes'
for _, module_name, _ in pkgutil.iter_modules([package.replace('.', '/')]):
  module = importlib.import_module(f'{package}.{module_name}')
  if hasattr(module, 'router'):
    app.include_router(getattr(module, 'router'), prefix=prefix)

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=5050, reload=True)
