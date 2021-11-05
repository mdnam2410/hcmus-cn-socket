# có 2 kiểu nút bấm
- là bấm vào thì context của nút đó thay đổi dựa trên trạng thái 
- là tác biệt từng tính năng đó ra từng nút

Ví dụ: start xong thì nút đó thay đổi text thành stop và sự kiện onCick thay đổi sang function khác

Vì lý do kỹ thuật code sẽ nhanh hơn nếu chọn cách 2 nên sẽ làm như vậy trước đã
nào rảnh chỉnh sau

để làm được cách 1 thì có thể tạo 1 class là ButtonBaseState có các thuộc tính state
mỗi khi render button đó sẽ switch case trạng thái để render cho phù hợp

Các nút bấm bị ảnh hưởng: 
- Connect / Disconnect
- Hook / Unhook
- Lock - Unlock


# Cách build file .py từ .ui
python -m PyQt5.uic.pyuic -x *.ui -o *.py

# Chú ý đường dẫn
sau khi build thì image vẫn còn path tương đối với thư mục ui
nên phải đổi lại 