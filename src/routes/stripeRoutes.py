import datetime
from pydantic import BaseModel,EmailStr
from fastapi import APIRouter, HTTPException, Depends
from src.config.index import appConfig
from src.services.clerkAuth import get_current_user_clerk_id
import stripe
from fastapi import Request
import os
from src.config.index import appConfig
from src.services.supabase import supabase
from datetime import datetime
import stripe 

router = APIRouter(tags=["stripeRoutes"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
DOMAIN = appConfig["domain"]




class CheckoutRequest(BaseModel):
    price_id: str
    email: EmailStr 


@router.post("/create-checkout-session")
def create_checkout_session(body: CheckoutRequest, clerk_user=Depends(get_current_user_clerk_id)):
    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": body.price_id, "quantity": 1}],
            customer_email=body.email,
            success_url=f"{DOMAIN}/billing/success",
            cancel_url=f"{DOMAIN}/billing/cancel",
            metadata={
                "clerk_user_id": clerk_user, 
            }
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    


@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, appConfig["stripe_webhook_secret"]
        )
    except Exception as e:
        return {"status": "error"}
    
    event_type = event['type']

    if event_type == "checkout.session.completed":

        session = event["data"]["object"]

        clerk_user_id = session["metadata"]["clerk_user_id"]
        subscription_id = session["subscription"]
        customer_id = session["customer"]
        subscription = stripe.Subscription.retrieve(subscription_id)
        status = subscription["status"]
           

        current_period_end = subscription["items"]["data"][0]["current_period_end"]
        
        readableDate = datetime.fromtimestamp(current_period_end).strftime("%Y-%m-%d %H:%M:%S") # This is not used anywhere
        print(readableDate)

        price_id = subscription["items"]["data"][0]["price"]["id"]

        PLAN_BY_PRICE_ID = {
            "price_1Sfi6LSC6OSw12xOJIdFTYKk": "hobby",
            "price_1Sfi6pSC6OSw12xOTbyvt0dN": "pro",
        }
        plan = PLAN_BY_PRICE_ID.get(price_id, "free")

        sub = stripe.Subscription.retrieve(subscription_id)
        try:
            update_subscription(
                clerk_user_id=clerk_user_id,
                stripe_customer_id=customer_id,
                stripe_subscription_id=subscription_id,
                plan=plan,
                status=status,
                current_period_end=readableDate
            )
        except Exception as e:
            print("Error updating subscription:", e)

    return {"status": "success"}


def update_subscription(clerk_user_id,stripe_customer_id,stripe_subscription_id,plan,status,current_period_end):

    print("Updating subscription for user:", clerk_user_id)
    print("Stripe Customer ID:", stripe_customer_id)
    print("Stripe Subscription ID:", stripe_subscription_id)
    print("Plan:", plan)
    print("Status:", status)
    print("Current Period End:", current_period_end)
    try:
        result = (
        supabase
        .table("subscriptions")
        .upsert(
            {
                "clerk_user_id": clerk_user_id,
                "stripe_customer_id": stripe_customer_id,
                "stripe_subscription_id": stripe_subscription_id,
                "plan": plan,
                "status": status,
                "current_period_end": current_period_end,
            },
            on_conflict="clerk_user_id",  
        )
        .execute()
        )
    except Exception as e:
        print("Error updating subscription:", e)
        return {"error": str(e)}
    return result.data[0] if result.data else None