from fastapi import FastAPI,Path


app = FastAPI()

@app.get("/users/{user_id}/contact-info")
def get_user_contact_info(
    user_id: str = Path(..., min_length=4, max_length=10)
) :
    return {"message":user_id}