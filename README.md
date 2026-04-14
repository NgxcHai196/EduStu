# EduStu

EduStu la ung dung desktop quan ly sinh vien viet bang `PyQt6`, to chuc theo huong `MVC` cho phan frontend. Repo hien tai chua gom backend; frontend giao tiep voi API qua HTTP va mac dinh goi den `http://localhost:8000`.

## Chuc nang hien co

- Dang nhap
- Dashboard tong quan
- Quan ly sinh vien
- Quan ly hoc phan
- Tra cuu va nhap diem
- Theo doi hoc phi va ghi nhan thanh toan
- Xuat bao cao Excel

## Cong nghe

- Python 3
- PyQt6
- requests

## Cau truc repo

```text
EduStu/
|-- Frontend/
|   |-- main.py
|   |-- controllers/
|   |   |-- auth.py
|   |   |-- base.py
|   |   |-- course.py
|   |   |-- grade.py
|   |   |-- report.py
|   |   |-- student.py
|   |   `-- tuition.py
|   |-- models/
|   |   |-- course.py
|   |   |-- grade.py
|   |   |-- student.py
|   |   |-- transcript.py
|   |   |-- tuition.py
|   |   `-- user.py
|   |-- utils/
|   |   |-- config.py
|   |   |-- helpers.py
|   |   `-- session.py
|   `-- views/
|       |-- base_view.py
|       |-- course_view.py
|       |-- dashboard_view.py
|       |-- grade_view.py
|       |-- login_view.py
|       |-- main_window.py
|       |-- report_view.py
|       |-- student_view.py
|       `-- tuition_view.py
|-- requirements.txt
`-- README.md
```

### mo ta giao dien
<img width="899" height="675" alt="Screenshot 2026-04-14 080459" src="https://github.com/user-attachments/assets/1d9c6b17-2153-4830-95e4-603b06b10d9d" />
<img width="916" height="720" alt="Screenshot 2026-04-14 080523" src="https://github.com/user-attachments/assets/4517aecc-5526-4ca0-b893-0fa64bb0a729" />
<img width="888" height="707" alt="Screenshot 2026-04-14 080548" src="https://github.com/user-attachments/assets/6547520f-e75a-438f-9933-33808eee1896" />
<img width="721" height="671" alt="Screenshot 2026-04-14 081926" src="https://github.com/user-attachments/assets/34fc198c-4208-4b0e-adc2-eb423b3a947d" />
<img width="933" height="696" alt="Screenshot 2026-04-14 081600" src="https://github.com/user-attachments/assets/1ed611ea-bf60-48ff-9284-832399a7c52e" />
<img width="887" height="721" alt="Screenshot 2026-04-14 080618" src="https://github.com/user-attachments/assets/dd98582a-4cae-416d-8ef4-e6963209dc84" />
<img width="862" height="735" alt="Screenshot 2026-04-14 080610" src="https://github.com/user-attachments/assets/952eb92f-a4f3-45b7-8106-69cb12419cf8" />
<img width="889" height="737" alt="Screenshot 2026-04-14 080601" src="https://github.com/user-attachments/assets/949454b2-a340-42fd-93a3-8dff307dd986" />


### mo ta chuc nang
<img width="722" height="679" alt="image" src="https://github.com/user-attachments/assets/db6590cf-1b20-48f6-80e7-ef2ee09e9d7c" />
<img width="706" height="698" alt="image" src="https://github.com/user-attachments/assets/c3070493-5150-4522-b441-eb2ee8fe085c" />
<img width="725" height="691" alt="image" src="https://github.com/user-attachments/assets/7b469473-9da6-4890-94f8-172dab0bc9bf" />
<img width="717" height="770" alt="image" src="https://github.com/user-attachments/assets/9bf81a67-4153-4fc3-999e-ddfd28c71200" />
<img width="710" height="641" alt="image" src="https://github.com/user-attachments/assets/a0094dd2-4324-4c0f-96d6-5b4d9a2be684" />
<img width="712" height="749" alt="image" src="https://github.com/user-attachments/assets/62a699ca-8ad4-44ab-95c2-2966cd5ee719" />


## Kien truc

Frontend duoc tach thanh 4 lop chinh:

- `views/`: giao dien PyQt6
- `controllers/`: validate du lieu, goi API, dieu phoi logic giao dien
- `models/`: dataclass va logic hien thi/nghiep vu nhe
- `utils/`: config, helper format, session dang nhap

`Frontend/main.py` la diem vao cua ung dung. Sau khi dang nhap thanh cong, app mo `MainWindow` va dieu huong sang cac man hinh chuc nang.

## API frontend dang su dung

Frontend hien tai ky vong backend co cac endpoint sau:

- `POST /auth/login`
- `PUT /auth/password`
- `GET /sinhvien`
- `GET /sinhvien/{mssv}`
- `POST /sinhvien`
- `PUT /sinhvien/{mssv}`
- `DELETE /sinhvien/{mssv}`
- `POST /sinhvien/import`
- `GET /hocphan`
- `POST /hocphan`
- `PUT /hocphan/{ma_hp}`
- `DELETE /hocphan/{ma_hp}`
- `GET /dangky/{mssv}`
- `POST /dangky`
- `DELETE /dangky/{id}`
- `GET /diem/{mssv}`
- `POST /diem`
- `PUT /diem/{id}`
- `GET /diem/{mssv}/gpa`
- `GET /hocphi`
- `GET /hocphi/conno`
- `POST /hocphi/thanhtoan`
- `GET /baocao/dashboard`
- `GET /baocao/thongke`
- `GET /baocao/export/excel`

## Cai dat

Tao moi truong ao va cai dependency:

```powershell
cd C:\Users\admin\EduStu
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Neu PowerShell chan script, chay tam:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Cach chay

Chay frontend:

```powershell
cd C:\Users\admin\EduStu\Frontend
python main.py
```

Hoac neu dang dung virtual environment o root repo:

```powershell
cd C:\Users\admin\EduStu
.\.venv\Scripts\python.exe .\Frontend\main.py
```

## Cau hinh

File cau hinh chinh nam o `Frontend/utils/config.py`.

Gia tri quan trong:

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

![alt text](assets/demo.png)