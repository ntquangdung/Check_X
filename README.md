# Twitter/X Batch Checker

Ban nay chi con phan CLI de chay tren CMD/PowerShell.

Tool phan loai username Twitter/X thanh:

- `live`
- `suspended`
- `die`
- `unknown`

## Cai dat

Can co:

- Python 3.10+
- Google Chrome hoac Chromium

Lenh cai:

```bash
pip install -r requirements.txt
```

## Cach chay

Nhap truc tiep username:

```bash
python cli_check.py -u jack openai elonmusk
```

Doc tu file text:

```bash
python cli_check.py -f usernames.txt
```

Doc file tren Desktop:

```bash
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt"
```

Luu ket qua ra CSV:

```bash
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt" -o result.csv
```

Neu muon mo browser de xem qua trinh:

```bash
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt" --show-browser
```
