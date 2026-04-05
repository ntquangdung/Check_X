# Twitter/X Batch Checker

## Thong tin du an

Twitter/X Batch Checker la tool CLI viet bang Python de kiem tra hang loat username Twitter/X.

Tool se phan loai moi username thanh 4 nhom:

- `live`
- `suspended`
- `die`
- `unknown`

Muc dich cua project:

- nhap nhieu username cung luc
- kiem tra tung profile tu dong
- in ket qua ra terminal
- xuat toan bo ket qua ra CSV
- xuat rieng danh sach username `live` ra file Excel `.xlsx`

## Quy trinh huong dan su dung

### 1. Yeu cau moi truong

- Windows
- Python 3.10+
- Google Chrome hoac Chromium

### 2. Cai dat

Mo `CMD` hoac `PowerShell`, vao thu muc project:

```bash
cd /d D:\X
```

Cai dependencies:

```bash
pip install -r requirements.txt
```

### 3. Chuan bi file username

Tao file `.txt`, moi dong mot username.

Vi du:

```text
LeoManda299953
YbarraTami39721
LoveLeone127393
```

Neu file nam tren Desktop:

```text
%USERPROFILE%\Desktop\kiemtraX.txt
```

### 4. Chay tool

Kiem tra tu file:

```bash
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt"
```

Kiem tra username nhap truc tiep:

```bash
python cli_check.py -u jack openai elonmusk
```

### 5. Xuat ket qua

Luu toan bo ket qua ra CSV:

```bash
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt" -o result.csv
```

Luu rieng username `live` ra Excel:

```bash
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt" --live-xlsx live_usernames.xlsx
```

Xuat ca CSV va Excel:

```bash
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt" -o result.csv --live-xlsx live_usernames.xlsx
```

### 6. Cac tuy chon bo sung

Mo browser de xem qua trinh:

```bash
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt" --show-browser
```

Tang timeout:

```bash
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt" --timeout 200
```

### 7. Cach doc ket qua

- `live`: tim thay `@username`
- `suspended`: tim thay `Account suspended`
- `die`: tim thay `This account doesn't exist`
- `unknown`: het timeout ma van khong xac nhan duoc 1 trong 3 truong hop tren

## Cong nghe su dung

- `Python`: ngon ngu chinh cua project
- `DrissionPage`: dieu khien Chromium de mo va doc profile Twitter/X
- `openpyxl`: tao file Excel `.xlsx` cho danh sach `live`
- `csv`: xuat toan bo ket qua ra file CSV
- `argparse`: nhan tham so dong lenh cho tool CLI

## Lenh mau day du

Chi kiem tra:

```bash
cd /d D:\X
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt"
```

Kiem tra va xuat Excel danh sach `live`:

```bash
cd /d D:\X
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt" --live-xlsx "%USERPROFILE%\Desktop\live_usernames.xlsx"
```

Kiem tra va xuat ca CSV + Excel:

```bash
cd /d D:\X
python cli_check.py -f "%USERPROFILE%\Desktop\kiemtraX.txt" -o "%USERPROFILE%\Desktop\result.csv" --live-xlsx "%USERPROFILE%\Desktop\live_usernames.xlsx"
```
