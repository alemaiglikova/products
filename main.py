from fastapi import FastAPI
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import psycopg2
import json
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Product:

    @staticmethod
    def select_rows_query(query: str) -> list[tuple]:
        with psycopg2.connect(user="pgs_usr", password="12345Qwerty!",
                              host="127.0.0.1", port="5432", dbname="pgs_db") as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                if rows is None:
                    raise Exception("not have objs")
                return rows
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    products = [
        {
            "id": x,
            "title": f"Бананы {x}",
            "price": round(1200.75 * x, 3),
            "count": round(20 / x, 3),
            "type_measure": "kg",
            "nomeklatura_id": f"{x}_Бананы_{x}"
        }
        for x in range(1, 30 + 1)
    ]
    products_list = []
    rows = Product.select_rows_query(
        "SELECT title, price, count, type_measure FROM products order by count desc, title asc;")
    print(rows, type(rows), type(rows[0]))

    products = [
        {
            "title": x[0],
            "price": x[1],
            "count": x[2],
            "type_measure": x[3],
        }
        for x in rows
    ]

    context = {"request": request, "products": products}
    return templates.TemplateResponse("ProductAll.html", context)