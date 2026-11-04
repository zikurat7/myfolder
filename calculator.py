import math
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="Calculator")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class Calculationz(BaseModel):
    a: float
    b: float
    operation: Literal["add", "subtract", "multiply", "divide"]


@app.get("/")
def calculator() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
    

@app.post("/api/calc")
def calculate(calculation: Calculationz) -> dict[str, float]:
    if not math.isfinite(calculation.a) or not math.isfinite(calculation.b):
        raise HTTPException(status_code=400, detail="Inputs must be finite numbers.")

    if calculation.operation == "add":
        result = calculation.a + calculation.b
    elif calculation.operation == "subtract":
        result = calculation.a - calculation.b
    elif calculation.operation == "multiply":
        result = calculation.a * calculation.b
    else:
        if calculation.b == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero.")
        result = calculation.a / calculation.b

    if not math.isfinite(result):
        raise HTTPException(status_code=400, detail="The result is outside the supported range.")

    return {"result": result}
