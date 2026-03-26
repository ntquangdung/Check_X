# Twitter/X Batch Checker

Web app Python dung de kiem tra hang loat username Twitter/X va phan loai:

- `alive`: tai khoan van truy cap duoc
- `suspended`: tai khoan da bi suspend
- `dead`: username khong ton tai, da doi ten, hoac trang profile khong con
- `unknown`: khong du tin hieu de ket luan

## Tinh nang

- Nhap nhieu username trong mot o textarea
- Ho tro tach username theo dong hoac dau phay
- Kiem tra hang loat va hien thi ket qua bang
- Su dung `DrissionPage` de dieu khien Chromium nhanh hon cach mo browser moi cho tung username

## Cai dat

Can co:

- Python 3.10+
- Google Chrome hoac Chromium

Lenh cai:

```bash
pip install -r requirements.txt
```

## Chay app web

```bash
python app.py
```

Mo trinh duyet tai:

```text
http://127.0.0.1:5000
```

## Chay nhanh tren CMD

Kiem tra bang danh sach username truyen truc tiep:

```bash
python cli_check.py -u jack openai elonmusk
```

Hoac truyen phan tach boi dau phay:

```bash
python cli_check.py -u "jack,openai,elonmusk"
```

Doc tu file text:

```bash
python cli_check.py -f usernames.txt
```

Tang toc bang nhieu worker song song:

```bash
python cli_check.py -f usernames.txt --workers 5
```

Luu ket qua ra CSV:

```bash
python cli_check.py -f usernames.txt -o result.csv
```

Mac dinh script se chay an browser.
Neu muon mo browser de xem qua trinh:

```bash
python cli_check.py -f usernames.txt --show-browser
```

## Luu y

- X/Twitter thay doi giao dien kha thuong xuyen, vi vay mot so keyword nhan dien co the can chinh sua trong file `checker.py`.
- Neu X chan yeu cau hoac bat dang nhap/captcha, mot so ket qua se roi vao `unknown`.
- De debug de hon, ban co the doi `headless=True` thanh `False` trong `BatchChecker`.
