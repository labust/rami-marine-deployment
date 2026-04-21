# PlanktoScope Extra Control Backend

Ovo je minimalna Python web aplikacija za Raspberry Pi koja može raditi paralelno s PlanktoScope sustavom.

## Što dobiješ

- FastAPI backend
- jednostavan HTML testni frontend na `/`
- REST API za paljenje i gašenje pumpi
- `systemd` servis za automatsko pokretanje pri bootu
- pristup s drugih računala u istoj mreži

## Zadani GPIO pinovi

- `pump1` -> GPIO17
- `pump2` -> GPIO27
- `pump3` -> GPIO22
- `pump4` -> GPIO23

To su dobri početni pinovi za dodatne pumpe uz PlanktoScope HAT.

## Struktura

- `main.py` - aplikacija
- `requirements.txt` - Python paketi
- `pump-control.service` - servis za auto-start
- `templates/index.html` - testno web sučelje

## Instalacija na Raspberry Pi

### 1. Kopiraj projekt

Kopiraj ovu mapu na Pi, npr. u:

```bash
/home/pi/planktoscope_extra_backend
```

### 2. Napravi virtual environment i instaliraj pakete

```bash
cd /home/pi/planktoscope_extra_backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Test ručnog pokretanja

```bash
cd /home/pi/planktoscope_extra_backend
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 5000
```

Otvori s računala u mreži:

```text
http://IP_RASPBERRYA:5000
```

ili ako lokalno ime radi:

```text
http://pkscope.local:5000
```

## API rute

### Status

```http
GET /health
```

### Popis pumpi

```http
GET /api/pumps
```

### Jedna pumpa

```http
GET /api/pumps/pump1
```

### Uključi pumpu

```http
POST /api/pumps/pump1/on
```

### Isključi pumpu

```http
POST /api/pumps/pump1/off
```

### Postavi stanje JSON-om

```http
POST /api/pumps/pump1
Content-Type: application/json

{
  "enabled": true
}
```

## Automatsko pokretanje pri bootu

Kopiraj servis:

```bash
sudo cp pump-control.service /etc/systemd/system/pump-control.service
sudo systemctl daemon-reload
sudo systemctl enable pump-control
sudo systemctl start pump-control
```

Provjera:

```bash
systemctl status pump-control
```

## Važno

- Nemoj spajati pumpe direktno na GPIO.
- Koristi MOSFET, driver ili relejni modul.
- Obavezno koristi zajednički GND između Pi-ja i vanjskog napajanja.

## Napomena za razvoj

Ako aplikaciju pokrećeš na običnom računalu, umjesto pravog GPIO-a koristi se mock način rada. Zato se kod može razvijati i testirati i bez Raspberry Pi-ja.
