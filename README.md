# EduStu

EduStu la du an quan ly sinh vien theo huong tach lop MVC, hien tai tap trung vao phan `Frontend` va cac model xu ly nghiep vu. Ma nguon dang o giai doan khoi tao cau truc, chua phai ban hoan chinh de chay full app.

## Tong quan

Du an huong toi cac chuc nang quan ly hoc vu co ban:

- Dang nhap, dang xuat, doi mat khau
- Quan ly sinh vien
- Quan ly hoc phan
- Dang ky hoc phan
- Nhap diem, tinh tong ket, quy doi GPA
- Theo doi hoc phi va cong no
- Tong hop dashboard va canh bao hoc vu

Diem dang chu y trong code hien tai:

- Cac model uu tien goi API qua `ApiClient`
- Neu backend chua san sang, model se fallback sang du lieu demo trong bo nho
- Logic nghiep vu duoc dat trong model, khong day sang view/controller

## Trang thai hien tai

Repo hien dang co:

- Thu muc `Frontend/Models` voi cac model nghiep vu chinh
- Thu muc rong cho `views`, `controllers`, `assets`
- File cau hinh rong `Frontend/utils/config.py`
- Moi Git repo, README va `.gitignore`

Repo hien chua co day du:

- File `Frontend/utils/api_client.py`
- File `Frontend/Models/demo_data.py`
- Cac controller thuc thi
- Cac view giao dien
- Diem vao chay chuong trinh, vi du `main.py`
- Ma nguon backend trong thu muc `Backend`

Noi cach khac, day la bo khung model va nghiep vu, chua phai ban co the chay giao dien ngay.

## Cau truc thu muc

```text
EduStu/
|-- Backend/
|-- Frontend/
|   |-- Models/
|   |   |-- auth_models.py
|   |   |-- student_model.py
|   |   |-- course_model.py
|   |   |-- enrollment_model.py
|   |   |-- grade_model.py
|   |   |-- tuition_model.py
|   |   `-- dashboard_model.py
|   |-- controllers/
|   |-- views/
|   |-- utils/
|   |   `-- config.py
|   `-- assets/
|-- .gitignore
`-- README.md
```

## Mo ta cac model

### `auth_models.py`

- Xu ly dang nhap, dang xuat, doi mat khau
- Uu tien goi API `/auth/...`
- Neu API loi thi fallback sang `DEMO_ACCOUNTS`

### `student_model.py`

- CRUD sinh vien
- Tim theo MSSV, ho ten, lop, trang thai
- Ho tro xoa mem qua `soft_delete()`
- Co ham lay bang diem cua mot sinh vien

### `course_model.py`

- CRUD hoc phan
- Co loc theo hoc ky
- Khi offline se thao tac tren `_cache`

### `enrollment_model.py`

- Dang ky, huy dang ky hoc phan theo hoc ky
- Luu danh sach hoc phan ma sinh vien da dang ky

### `grade_model.py`

- Chua logic nghiep vu tinh diem:
  - `tinh_tong_ket()`
  - `xep_loai_diem()`
  - `quy_doi_sang_gpa4()`
  - `xep_loai_hoc_luc()`
- Ho tro luu diem hang loat hoac tung sinh vien
- Tinh GPA theo tin chi

### `tuition_model.py`

- Theo doi hoc phi theo hoc ky
- Ghi nhan thanh toan
- Tinh trang thai:
  - Da dong
  - Dong thieu
  - Chua dong
- Tong hop tong thu va cong no

### `dashboard_model.py`

- Tong hop so lieu tu sinh vien, hoc phan, diem, hoc phi
- Lay thong ke dashboard
- Tao danh sach canh bao hoc vu
- Lay danh sach sinh vien moi

## Dinh huong kien truc

Code hien tai dang theo y tuong:

- `Models`: nghiep vu va truy cap du lieu
- `Controllers`: nhan su kien tu giao dien, goi model, xu ly loi
- `Views`: giao dien PyQt hoac desktop GUI
- `utils`: cau hinh, API client, helper dung chung

Mot diem can luu y la ten thu muc dang la `Frontend/Models` viet hoa, trong khi nhieu file import theo dang `from models...`. Khi hoan thien du an, ban nen thong nhat ten package de tranh loi import tren moi truong phan biet hoa thuong.

## Moi truong du kien

Tu `Frontend/venv` co the thay du an dang du kien dung:

- Python 3.11
- PyQt5
- requests
- openpyxl

## Cai dat de phat trien tiep

Neu ban muon hoan thien project tu trang thai hien tai, quy trinh hop ly la:

1. Tao virtual environment moi
2. Cai cac thu vien can thiet
3. Bo sung `api_client.py`
4. Bo sung `demo_data.py`
5. Viet `views/`, `controllers/` va file chay chinh
6. Neu co backend thi dinh nghia cac API ma model dang goi

Vi du:

```powershell
cd Frontend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install PyQt5 requests openpyxl
```

## Cac API ma frontend dang ky vong

Cac model hien tai dang tham chieu den nhung endpoint sau:

- `POST /auth/login`
- `POST /auth/logout`
- `POST /auth/change-password`
- `GET /dashboard/stats`
- `GET /dashboard/warnings`
- `GET /students`
- `GET /students/{id}`
- `GET /students/{id}/transcript`
- `GET /students/{id}/gpa`
- `POST /students`
- `PUT /students/{id}`
- `GET /courses`
- `GET /courses/{id}`
- `POST /courses`
- `PUT /courses/{id}`
- `DELETE /courses/{id}`
- `GET /grades`
- `POST /grades/bulk`
- `POST /grades/upsert`
- `GET /enrollments`
- `POST /enrollments`
- `DELETE /enrollments/{id}`
- `GET /tuition`
- `GET /tuition/debtors`
- `POST /tuition/pay`

## Viec nen lam tiep

- Tao `requirements.txt`
- Viet `api_client.py`
- Viet `demo_data.py`
- Dong bo ten package `Models` va import `models`
- Them unit test cho logic tinh diem, GPA va hoc phi
- Bo sung giao dien va controller
- Xay dung backend FastAPI hoac chinh sua model de phu hop backend san co
