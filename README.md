# Twitter/X Batch Checker

Tool CLI de kiem tra hang loat username Twitter/X bang Python + DrissionPage.

Trang thai dau ra:

- `live`
- `suspended`
- `die`
- `unknown`

## Yeu cau

- Windows
- Python 3.10+
- Google Chrome hoac Chromium

## Cai dat

Mo `CMD` hoac `PowerShell`, di chuyen vao thu muc project:

```bash
cd /d D:\X
```

Cai thu vien:

```bash
pip install -r requirements.txt
```

## Chuan bi file username

Tao file `.txt`, moi dong 1 username.

Vi du file `kiemtraX.txt`:

```text
LeoManda299953
YbarraTami39721
LoveLeone127393
```

Neu file nam tren Desktop:

```text
%USERPROFILE%\Desktop\kiemtraX.txt
```

## Cach chay co ban

### 1. Kiem tra tu file text

```bash
cd /d D:\X
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt"
```

Tool se:

- doc tung username
- mo profile X/Twitter
- in tien do `Dang kiem tra x/y`
- tra bang ket qua trong terminal

### 2. Kiem tra username nhap truc tiep

```bash
python cli_check.py -u jack openai elonmusk
```

## Cac tuy chon output

### 1. Luu toan bo ket qua ra CSV

```bash
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt" -o result.csv
```

### 2. Luu rieng username `live` ra file Excel

```bash
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt" --live-xlsx live_usernames.xlsx
```

File Excel se co 1 sheet:

- `live_usernames`

Va 1 cot:

- `username`

### 3. Vua xuat CSV, vua xuat Excel `live`

```bash
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt" -o result.csv --live-xlsx live_usernames.xlsx
```

## Cac tuy chon khac

### Mo browser de xem qua trinh

```bash
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt" --show-browser
```

### Tang timeout

Mac dinh timeout la `100` giay cho moi profile.

Neu muon tang timeout:

```bash
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt" --timeout 200
```

## Cach doc ket qua

Tool kiem tra theo logic:

- `live`: tim thay `@username`
- `suspended`: tim thay `Account suspended`
- `die`: tim thay `This account doesn't exist`
- `unknown`: het timeout ma van khong xac nhan duoc 1 trong 3 truong hop tren

## Lenh mau day du

### Chi kiem tra

```bash
cd /d D:\X
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt"
```

### Kiem tra va xuat Excel danh sach live

```bash
cd /d D:\X
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt" --live-xlsx "%USERPROFILE%\Desktop\live_usernames.xlsx"
```

### Kiem tra va xuat ca CSV + Excel

```bash
cd /d D:\X
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt" -o "%USERPROFILE%\Desktop\result.csv" --live-xlsx "%USERPROFILE%\Desktop\live_usernames.xlsx"
```
