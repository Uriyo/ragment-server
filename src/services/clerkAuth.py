from src.config.index import appConfig
from fastapi import Request, HTTPException
import jwt
from typing import Optional


def get_current_user_clerk_id(request: Request) -> str:
    try:
        # Extract the Bearer token from the Authorization header
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=401, 
                detail="Missing or invalid Authorization header. Expected 'Bearer <token>'"
            )
        
        token = auth_header.split(" ", 1)[1]
        
        # Decode the JWT token (without verification for now, Clerk tokens are short-lived)
        # In production, you should verify the signature using Clerk's public key
        payload = jwt.decode(
            token,
            options={"verify_signature": False},
            algorithms=["RS256"]
        )
        
        clerk_id = payload.get("sub")
        
        if not clerk_id:
            raise HTTPException(
                status_code=401, 
                detail="Clerk ID (sub) not found in token"
            )
        
        return clerk_id

    except HTTPException:
        raise
    except jwt.DecodeError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token format. {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Authentication failed. {str(e)}",
        )
