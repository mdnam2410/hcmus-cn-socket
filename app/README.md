# Chú ý
Do mình cấu trúc lại theo kiểu chia module và package, do đó để chạy code được thì phải thêm một cái environment variable tên là PYTHONPATH (dùng PowerShell hoặc là mở bằng GUI của Windows).
```
SET PYTHONPATH=C:\path\to\project\directory
```

# Giải thích về cấu trúc thư mục `app`
---

`app` có ba thư mục con:
* `core`: định nghĩa hàm và class dùng chung cho cả client và server
* `client`: định nghĩa hàm và class sử dụng cho client
* `server`: định nghĩa hàm và class sử dụng cho server

## `core`
`core` chứa các file:
* `protocol.py`: định nghĩa
    * status code (đổi từ error code sang status code :v)
    * status message
    * server port
    * mã hóa gói tin
    * buffer cho `socket.recv`
    * các hàm `encode`, `decode` dùng để định dạng gói tin
    * các hàm `send`, `receive` định nghĩa cách gửi gói tin bằng socket
    * class `Message` đại diện cho một gói tin, `Message` có 2 class con:
        * `Request`: đại diện cho một request từ client
        * `Response`: đại diện cho một response từ server
* `exceptions.py`: định nghĩa các exception có thể có
* `utils.py`: định nghĩa các hàm khác

## `client`
Định nghĩa client. Code của client bắt đầu chạy trong file `main.py`. Định nghĩa GUI trong `ui`. Định nghĩa các tính năng cần thiết khác trong `packages`.

Trong `packages` có file `portal.py` dùng để định nghĩa class `Portal`. Class này dùng để:
* Wrap around cho socket của client
    * Mở/đóng kết nối đến server
    * Gửi, nhận gói tin thông qua hai hàm `send` và `receive` trong `core/protocol.py`
* Định nghĩa các hàm để gửi lệnh cho server
Xem thêm ở cuối file có demo.

## `server`
Tương tự như `client`. Code chạy trong `main.py`, GUI trong `ui`, tính năng trong `packages`.

Trong `packages` có file `service.py` định nghĩa class `Service`. Class này dùng để:
* Wrap around cho socket của server
* Nhận và gửi gói tin từ client
* Gọi các hàm phục vụ client theo yêu cầu từ gói tin
Xem thêm ở cuối file có demo.

Các file còn lại định nghĩa các tính năng của đồ án. Mình sẽ định nghĩa từng tính năng bằng cách tạo module trong thư mục `packages` này.

Vậy thôi :))