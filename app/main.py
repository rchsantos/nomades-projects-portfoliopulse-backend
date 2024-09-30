import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import user, auth, portfolio

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

# Including the routers.
app.include_router(auth.router, prefix=prefix)
app.include_router(user.router, prefix=prefix)
app.include_router(portfolio.router, prefix=prefix)

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=5050, reload=True)
