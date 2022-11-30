# workshop

## Requirement
- Python3
- Docker (optional)

## For local workspace
- Use python virtualenv

```bash
virtualenv -p `which python3` websummit
source websummit/bin/python
```
- install requirement packages
```bash
pip install -r requirements
```
- Start python script
```bash
python Web/CreateWebImage.py
```

## For Docker
- build image
```bash
docker build -t summit_web:latest .
```
- Start container
```bash
docker run --rm summit_web:latest
```