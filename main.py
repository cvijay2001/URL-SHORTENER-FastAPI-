from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import shortuuid
from fastapi.middleware.cors import CORSMiddleware
import models 
import database
from schemas import URLShortener
from fastapi.responses import RedirectResponse
# from starlette.responses import RedirectResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend domain or list of allowed domains
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Add "OPTIONS" method
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/{uni_code}")
def redirect_to_original_url(uni_code: str, db: Session = Depends(get_db)):
    url_shortener = db.query(models.URLShortenerModel).filter((models.URLShortenerModel.uni_code == uni_code) | (models.URLShortenerModel.alias == uni_code)).first()
    print("url_shortener:",url_shortener)
    if url_shortener is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=url_shortener.og_url)
    return {"original_url": url_shortener.og_url}



from fastapi import HTTPException

@app.post("/url_shortener/")
def create_url_shortener(url_shortener: URLShortener, db: Session = Depends(get_db)):
    try:
        if url_shortener.alias:
            # Check if the provided alias already exists
            existing_alias = db.query(models.URLShortenerModel).filter((models.URLShortenerModel.alias == url_shortener.alias) | (models.URLShortenerModel.uni_code == url_shortener.alias)).first()

            print("Existing alias: --------> ",existing_alias )

            if existing_alias:
                return {"error": "Alias already exists"}
            short_url = f"http://127.0.0.1:8000/{url_shortener.alias}"
            db_url_shortener = models.URLShortenerModel(alias=url_shortener.alias, og_url=url_shortener.og_url, short_url=short_url)
            
        else:
            # Generate a unique short code
            short_code = shortuuid.uuid()[:8]

            # Construct short URL
            short_url = f"http://127.0.0.1:8000/{short_code}"

            db_url_shortener = models.URLShortenerModel(uni_code=short_code, og_url=url_shortener.og_url, short_url=short_url)
        db.add(db_url_shortener)
        db.commit()
        db.refresh(db_url_shortener)
        
        return db_url_shortener
    except Exception as e:
        # Handle exceptions
        raise HTTPException(status_code=500, detail="Internal Server Error")






