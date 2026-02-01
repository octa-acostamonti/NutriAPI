import math
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session, load_only
from .schemas import (
    ResponseProteina, ResponseCarbohidratos, ResponseGrasa, ResponseProductos,
    ResponseRetailerProduct, ResponseEnrichedProduct
)
from typing import List, Optional


def safe_float(val):
    """Convert NaN/inf to None for JSON compatibility."""
    if val is None:
        return None
    if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
        return None
    return val

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NutriAPI",
    description="API de información nutricional de productos alimenticios en Argentina",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return "NutriAPI © - Datos de Open Food Facts"


@app.get("/productos/", response_model=List[ResponseProductos])
def get_productos(
    db: Session = Depends(get_db),
    limit: int = Query(default=100, le=1000),
    offset: int = Query(default=0, ge=0),
):
    """Get all products with pagination."""
    productos = db.query(models.Productos).offset(offset).limit(limit).all()
    return productos


@app.get("/productos/{barcode}", response_model=ResponseProductos)
def get_producto_by_barcode(barcode: str, db: Session = Depends(get_db)):
    """Get a single product by its barcode."""
    producto = db.query(models.Productos).filter(models.Productos.barcode == barcode).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@app.get("/buscar/", response_model=List[ResponseProductos])
def buscar_productos(
    q: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
    limit: int = Query(default=50, le=200),
):
    """Search products by name."""
    productos = (
        db.query(models.Productos)
        .filter(models.Productos.producto.ilike(f"%{q}%"))
        .limit(limit)
        .all()
    )
    return productos


@app.get("/proteinas/", response_model=List[ResponseProteina])
def get_proteinas(db: Session = Depends(get_db)):
    """Get protein info for all products."""
    proteina = db.query(models.Productos).options(
        load_only(models.Productos.producto, models.Productos.marca, models.Productos.proteina_g_100g, models.Productos.serving_size)
    ).all()
    return proteina


@app.get("/grasas/", response_model=List[ResponseGrasa])
def get_grasas(db: Session = Depends(get_db)):
    """Get fat info for all products."""
    grasa = db.query(models.Productos).options(
        load_only(models.Productos.producto, models.Productos.marca, models.Productos.grasa_g_100g, models.Productos.serving_size)
    ).all()
    return grasa


@app.get("/carbohidratos/", response_model=List[ResponseCarbohidratos])
def get_carbohidratos(db: Session = Depends(get_db)):
    """Get carbohydrate info for all products."""
    carbohidratos = db.query(models.Productos).options(
        load_only(models.Productos.producto, models.Productos.marca, models.Productos.carbohidrato_g_100g, models.Productos.serving_size)
    ).all()
    return carbohidratos


@app.get("/retailers/", response_model=List[str])
def get_retailers(db: Session = Depends(get_db)):
    """Get list of available retailers."""
    retailers = db.query(models.RetailerProducts.retailer).distinct().all()
    return [r[0] for r in retailers]


@app.get("/retailers/{retailer}/productos/", response_model=List[ResponseRetailerProduct])
def get_retailer_products(
    retailer: str,
    db: Session = Depends(get_db),
    limit: int = Query(default=100, le=1000),
    offset: int = Query(default=0, ge=0),
):
    """Get products from a specific retailer."""
    products = (
        db.query(models.RetailerProducts)
        .filter(models.RetailerProducts.retailer == retailer.lower())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return products


@app.get("/retailers/{retailer}/buscar/", response_model=List[ResponseRetailerProduct])
def buscar_retailer_products(
    retailer: str,
    q: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
    limit: int = Query(default=50, le=200),
):
    """Search products in a retailer by name."""
    products = (
        db.query(models.RetailerProducts)
        .filter(
            models.RetailerProducts.retailer == retailer.lower(),
            models.RetailerProducts.product_name.ilike(f"%{q}%")
        )
        .limit(limit)
        .all()
    )
    return products


@app.get("/enriched/", response_model=List[ResponseEnrichedProduct])
def get_enriched_products(
    retailer: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    limit: int = Query(default=100, le=1000),
    offset: int = Query(default=0, ge=0),
):
    """Get retailer products enriched with nutritional data from Open Food Facts."""
    query = db.query(models.RetailerProducts)
    
    if retailer:
        query = query.filter(models.RetailerProducts.retailer == retailer.lower())
    
    retailer_products = query.offset(offset).limit(limit).all()
    
    enriched = []
    for rp in retailer_products:
        result = {
            "id": rp.id,
            "retailer": rp.retailer,
            "ean": rp.ean,
            "sku": rp.sku,
            "product_name": rp.product_name,
            "brand": rp.brand,
            "price": rp.price,
            "list_price": rp.list_price,
            "category": rp.category,
            "image_url": rp.image_url,
            "product_url": rp.product_url,
            "nutriscore_grade": None,
            "nova_group": None,
            "serving_size": None,
            "serving_quantity_g": None,
            "product_quantity_g": None,
            "caloria_kcal_100g": None,
            "proteina_g_100g": None,
            "grasa_g_100g": None,
            "carbohidrato_g_100g": None,
            "caloria_kcal_serving": None,
            "proteina_g_serving": None,
            "grasa_g_serving": None,
            "carbohidrato_g_serving": None,
            "allergens": None,
            "ingredients_text": None,
        }
        
        if rp.ean:
            nutri = db.query(models.Productos).filter(models.Productos.barcode == rp.ean).first()
            if nutri:
                result["nutriscore_grade"] = nutri.nutriscore_grade
                result["nova_group"] = nutri.nova_group
                result["serving_size"] = nutri.serving_size
                result["serving_quantity_g"] = safe_float(nutri.serving_quantity_g)
                result["product_quantity_g"] = safe_float(nutri.product_quantity_g)
                result["caloria_kcal_100g"] = safe_float(nutri.caloria_kcal_100g)
                result["proteina_g_100g"] = safe_float(nutri.proteina_g_100g)
                result["grasa_g_100g"] = safe_float(nutri.grasa_g_100g)
                result["carbohidrato_g_100g"] = safe_float(nutri.carbohidrato_g_100g)
                result["caloria_kcal_serving"] = safe_float(nutri.caloria_kcal_serving)
                result["proteina_g_serving"] = safe_float(nutri.proteina_g_serving)
                result["grasa_g_serving"] = safe_float(nutri.grasa_g_serving)
                result["carbohidrato_g_serving"] = safe_float(nutri.carbohidrato_g_serving)
                result["allergens"] = nutri.allergens
                result["ingredients_text"] = nutri.ingredients_text
        
                enriched.append(result)
    
    return enriched


@app.get("/enriched/{ean}", response_model=ResponseEnrichedProduct)
def get_enriched_product_by_ean(ean: str, db: Session = Depends(get_db)):
    """Get a single retailer product enriched with nutritional data by EAN."""
    rp = db.query(models.RetailerProducts).filter(models.RetailerProducts.ean == ean).first()
    
    if not rp:
        raise HTTPException(status_code=404, detail="Producto no encontrado en retailers")
    
    result = {
        "id": rp.id,
        "retailer": rp.retailer,
        "ean": rp.ean,
        "sku": rp.sku,
        "product_name": rp.product_name,
        "brand": rp.brand,
        "price": rp.price,
        "list_price": rp.list_price,
        "category": rp.category,
        "image_url": rp.image_url,
        "product_url": rp.product_url,
        "nutriscore_grade": None,
        "nova_group": None,
        "serving_size": None,
        "serving_quantity_g": None,
        "product_quantity_g": None,
        "caloria_kcal_100g": None,
        "proteina_g_100g": None,
        "grasa_g_100g": None,
        "carbohidrato_g_100g": None,
        "caloria_kcal_serving": None,
        "proteina_g_serving": None,
        "grasa_g_serving": None,
        "carbohidrato_g_serving": None,
        "allergens": None,
        "ingredients_text": None,
    }
    
    nutri = db.query(models.Productos).filter(models.Productos.barcode == ean).first()
    if nutri:
        result["nutriscore_grade"] = nutri.nutriscore_grade
        result["nova_group"] = nutri.nova_group
        result["serving_size"] = nutri.serving_size
        result["serving_quantity_g"] = safe_float(nutri.serving_quantity_g)
        result["product_quantity_g"] = safe_float(nutri.product_quantity_g)
        result["caloria_kcal_100g"] = safe_float(nutri.caloria_kcal_100g)
        result["proteina_g_100g"] = safe_float(nutri.proteina_g_100g)
        result["grasa_g_100g"] = safe_float(nutri.grasa_g_100g)
        result["carbohidrato_g_100g"] = safe_float(nutri.carbohidrato_g_100g)
        result["caloria_kcal_serving"] = safe_float(nutri.caloria_kcal_serving)
        result["proteina_g_serving"] = safe_float(nutri.proteina_g_serving)
        result["grasa_g_serving"] = safe_float(nutri.grasa_g_serving)
        result["carbohidrato_g_serving"] = safe_float(nutri.carbohidrato_g_serving)
        result["allergens"] = nutri.allergens
        result["ingredients_text"] = nutri.ingredients_text
    
    return result
