from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field


# --- GPIO layer ------------------------------------------------------------
# Works on a Raspberry Pi with RPi.GPIO installed.
# Falls back to an in-memory mock on non-Pi machines so development is easy.

try:
    import RPi.GPIO as GPIO  # type: ignore

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO_AVAILABLE = False
except Exception:
    GPIO = None
    GPIO_AVAILABLE = False


# --- Pump model ------------------------------------------------------------

@dataclass
class Pump:
    name: str
    pin: int
    calibration_ml_per_sec: float
    active_high: bool = True
    is_running: bool = False
    current_volume_ml: float = 0.0
    started_at: Optional[float] = None
    stop_requested: bool = False


DEFAULT_PUMPS: List[Pump] = [
    Pump(name="pump1", pin=17, calibration_ml_per_sec=1.8),
    Pump(name="pump2", pin=27, calibration_ml_per_sec=1.8),
    Pump(name="pump3", pin=22, calibration_ml_per_sec=1.8),
]


# --- GPIO controllers ------------------------------------------------------

class MockGPIOController:
    def __init__(self, pumps: List[Pump]) -> None:
        self._states: Dict[str, bool] = {pump.name: False for pump in pumps}
        self._pumps = {pump.name: pump for pump in pumps}

    def setup(self) -> None:
        return

    def set_state(self, pump_name: str, enabled: bool) -> bool:
        self._require_pump(pump_name)
        self._states[pump_name] = enabled
        return self._states[pump_name]

    def get_state(self, pump_name: str) -> bool:
        self._require_pump(pump_name)
        return self._states[pump_name]

    def get_all(self) -> Dict[str, bool]:
        return dict(self._states)

    def cleanup(self) -> None:
        return

    def _require_pump(self, pump_name: str) -> None:
        if pump_name not in self._pumps:
            raise KeyError(pump_name)


class RaspberryGPIOController:
    def __init__(self, pumps: List[Pump]) -> None:
        self._pumps = {pump.name: pump for pump in pumps}

    def setup(self) -> None:
        for pump in self._pumps.values():
            GPIO.setup(pump.pin, GPIO.OUT, initial=self._off_level(pump))

    def set_state(self, pump_name: str, enabled: bool) -> bool:
        pump = self._require_pump(pump_name)
        GPIO.output(pump.pin, self._on_level(pump) if enabled else self._off_level(pump))
        return self.get_state(pump_name)

    def get_state(self, pump_name: str) -> bool:
        pump = self._require_pump(pump_name)
        raw = GPIO.input(pump.pin)
        return raw == self._on_level(pump)

    def get_all(self) -> Dict[str, bool]:
        return {name: self.get_state(name) for name in self._pumps}

    def cleanup(self) -> None:
        GPIO.cleanup()

    def _require_pump(self, pump_name: str) -> Pump:
        pump = self._pumps.get(pump_name)
        if pump is None:
            raise KeyError(pump_name)
        return pump

    @staticmethod
    def _on_level(pump: Pump) -> int:
        return GPIO.HIGH if pump.active_high else GPIO.LOW

    @staticmethod
    def _off_level(pump: Pump) -> int:
        return GPIO.LOW if pump.active_high else GPIO.HIGH


controller = RaspberryGPIOController(DEFAULT_PUMPS) if GPIO_AVAILABLE else MockGPIOController(DEFAULT_PUMPS)
controller.setup()


# --- Helpers ---------------------------------------------------------------

pump_map: Dict[str, Pump] = {pump.name: pump for pump in DEFAULT_PUMPS}
pump_threads: Dict[str, threading.Thread] = {}
pump_lock = threading.Lock()


def get_pump_or_404(pump_name: str) -> Pump:
    pump = pump_map.get(pump_name)
    if pump is None:
        raise HTTPException(status_code=404, detail="Pumpa nije pronađena")
    return pump


def build_pump_data(pump: Pump) -> dict:
    return {
        "name": pump.name,
        "pin": pump.pin,
        "enabled": controller.get_state(pump.name),
        "calibration_ml_per_sec": pump.calibration_ml_per_sec,
        "is_running": pump.is_running,
        "current_volume_ml": pump.current_volume_ml,
        "started_at": pump.started_at,
    }


def run_dispense(pump: Pump, volume_ml: float) -> None:
    duration = volume_ml / pump.calibration_ml_per_sec

    pump.is_running = True
    pump.current_volume_ml = volume_ml
    pump.started_at = time.time()
    pump.stop_requested = False

    controller.set_state(pump.name, True)

    start = time.time()
    try:
        while True:
            if pump.stop_requested:
                break
            elapsed = time.time() - start
            if elapsed >= duration:
                break
            time.sleep(0.05)
    finally:
        controller.set_state(pump.name, False)
        pump.is_running = False
        pump.current_volume_ml = 0.0
        pump.started_at = None
        pump.stop_requested = False


# --- FastAPI app -----------------------------------------------------------

app = FastAPI(title="PlanktoScope Extra Control", version="0.2.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class PumpCommand(BaseModel):
    enabled: bool = Field(..., description="True = uključi pumpu, False = isključi pumpu")


class DispenseCommand(BaseModel):
    volume_ml: float = Field(..., gt=0, description="Volumen u mililitrima")


class CalibrationCommand(BaseModel):
    calibration_ml_per_sec: float = Field(..., gt=0, description="Kalibracija pumpe u mL/s")


@app.get("/health")
def health() -> dict:
    return {
        "ok": True,
        "gpio_mode": "raspberry" if GPIO_AVAILABLE else "mock",
        "pumps": [
            {
                "name": p.name,
                "pin": p.pin,
                "calibration_ml_per_sec": p.calibration_ml_per_sec,
            }
            for p in DEFAULT_PUMPS
        ],
    }


@app.get("/api/pumps")
def list_pumps() -> dict:
    return {"items": [build_pump_data(pump) for pump in DEFAULT_PUMPS]}


@app.get("/api/pumps/{pump_name}")
def get_pump(pump_name: str) -> dict:
    pump = get_pump_or_404(pump_name)
    return build_pump_data(pump)


@app.post("/api/pumps/{pump_name}")
def set_pump(pump_name: str, payload: PumpCommand) -> dict:
    pump = get_pump_or_404(pump_name)

    if pump.is_running and not payload.enabled:
        pump.stop_requested = True

    try:
        state = controller.set_state(pump.name, payload.enabled)
    except KeyError:
        raise HTTPException(status_code=404, detail="Pumpa nije pronađena")

    return {
        "ok": True,
        "name": pump.name,
        "pin": pump.pin,
        "enabled": state,
    }


@app.post("/api/pumps/{pump_name}/on")
def pump_on(pump_name: str) -> dict:
    return set_pump(pump_name, PumpCommand(enabled=True))


@app.post("/api/pumps/{pump_name}/off")
def pump_off(pump_name: str) -> dict:
    return set_pump(pump_name, PumpCommand(enabled=False))


@app.post("/api/pumps/{pump_name}/dispense")
def dispense_volume(pump_name: str, payload: DispenseCommand) -> dict:
    pump = get_pump_or_404(pump_name)

    with pump_lock:
        if pump.is_running:
            raise HTTPException(status_code=409, detail="Pumpa već radi")

        thread = threading.Thread(
            target=run_dispense,
            args=(pump, payload.volume_ml),
            daemon=True,
        )
        pump_threads[pump.name] = thread
        thread.start()

    duration_sec = payload.volume_ml / pump.calibration_ml_per_sec

    return {
        "ok": True,
        "name": pump.name,
        "volume_ml": payload.volume_ml,
        "calibration_ml_per_sec": pump.calibration_ml_per_sec,
        "estimated_duration_sec": duration_sec,
    }


@app.post("/api/pumps/{pump_name}/stop")
def stop_dispense(pump_name: str) -> dict:
    pump = get_pump_or_404(pump_name)

    if not pump.is_running:
        return {
            "ok": True,
            "name": pump.name,
            "message": "Pumpa nije bila aktivna",
        }

    pump.stop_requested = True
    return {
        "ok": True,
        "name": pump.name,
        "message": "Zaustavljanje zatraženo",
    }


@app.post("/api/pumps/{pump_name}/calibration")
def set_calibration(pump_name: str, payload: CalibrationCommand) -> dict:
    pump = get_pump_or_404(pump_name)

    if pump.is_running:
        raise HTTPException(status_code=409, detail="Ne možeš mijenjati kalibraciju dok pumpa radi")

    pump.calibration_ml_per_sec = payload.calibration_ml_per_sec

    return {
        "ok": True,
        "name": pump.name,
        "calibration_ml_per_sec": pump.calibration_ml_per_sec,
    }


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    pumps = [build_pump_data(pump) for pump in DEFAULT_PUMPS]
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "pumps": pumps,
            "gpio_mode": "raspberry" if GPIO_AVAILABLE else "mock",
        },
    )