import pygame
import random
import sys

# Khởi tạo Pygame
pygame.init()

# Cấu hình màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Five Nights at Freddy's 1 - Python Edition")

# Màu sắc (Dùng làm hình nền tạm thời nếu không có ảnh)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)

# Đồng hồ điều khiển FPS
clock = pygame.time.Clock()
FPS = 30

# Font chữ
font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 50)

# --- TRẠNG THÁI TRÒ CHƠI ---
power = 100.0          # Phần trăm pin
time_am = 12           # Thời gian bắt đầu (12 AM)
game_over = False
win = False

left_door = False      # Cửa trái đóng/mở
right_door = False     # Cửa phải đóng/mở
left_light = False     # Đèn trái bật/tắt
right_light = False    # Đèn phải bật/tắt

camera_open = False    # Trạng thái mở camera
current_cam = "CAM 1"  # Camera đang xem

# Vị trí của Freddy: 1 (Sân khấu) -> 2 (Hành lang) -> 3 (Cạnh cửa trái) -> 4 (Trong phòng - Jumpscare)
freddy_pos = 1 

# --- SỰ KIỆN THEO THỜI GIAN (Custom Events) ---
TICK_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TICK_EVENT, 1000) # Mỗi 1 giây chạy 1 lần

FREDDY_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(FREDDY_EVENT, 5000) # Mỗi 5 giây Freddy có cơ hội di chuyển

# Hàm vẽ nút bấm
def draw_button(text, rect, color, text_color=WHITE):
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, WHITE, rect, 2)
    txt = font.render(text, True, text_color)
    screen.blit(txt, (rect[0] + (rect[2] - txt.get_width())//2, rect[1] + (rect[3] - txt.get_height())//2))

# --- VÒNG LẶP CHÍNH CỦA TRÒ CHƠI ---
running = True
sec_counter = 0

while running:
    screen.fill(BLACK)
    
    # 1. XỬ LÝ SỰ KIỆN (INPUT)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if not game_over and not win:
            # Sự kiện đếm giây (Pin và Thời gian)
            if event.type == TICK_EVENT:
                # Tính lượng pin tiêu thụ dựa trên các thiết bị đang bật
                drain = 0.1 # Tiêu hao cơ bản
                if left_door: drain += 0.5
                if right_door: drain += 0.5
                if left_light: drain += 0.3
                if right_light: drain += 0.3
                if camera_open: drain += 0.4
                
                power -= drain
                if power <= 0:
                    power = 0
                    game_over = True # Hết pin = Thua (Freddy đến)

                # Cập nhật thời gian (Mỗi 45 giây thực tế lên 1 tiếng trong game)
                sec_counter += 1
                if sec_counter >= 45:
                    sec_counter = 0
                    if time_am == 12:
                        time_am = 1
                    else:
                        time_am += 1
                    if time_am == 6:
                        win = True

            # Sự kiện Freddy di chuyển
            if event.type == FREDDY_EVENT and not camera_open:
                # AI của Freddy: Tỉ lệ 50% di chuyển tiến lên
                if random.randint(1, 100) > 50:
                    if freddy_pos < 3:
                        freddy_pos += 1
                    elif freddy_pos == 3:
                        # Nếu đang ở sát cửa trái mà cửa đóng -> Bị bật lại sân khấu
                        if left_door:
                            freddy_pos = 1
                        else:
                            freddy_pos = 4 # Vào phòng -> Jumpscare!

            # Sự kiện Click chuột
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                if not camera_open:
                    # Click nút Cửa trái
                    if 20 <= mx <= 100 and 200 <= my <= 250:
                        left_door = not left_door
                    # Click nút Đèn trái
                    if 20 <= mx <= 100 and 270 <= my <= 320:
                        left_light = not left_light
                    # Click nút Cửa phải
                    if 700 <= mx <= 780 and 200 <= my <= 250:
                        right_door = not right_door
                    # Click nút Đèn phải
                    if 700 <= mx <= 780 and 270 <= my <= 320:
                        right_light = not right_light
                else:
                    # Chọn các phòng Camera
                    if 500 <= mx <= 600 and 400 <= my <= 450: current_cam = "CAM 1"
                    if 620 <= mx <= 720 and 400 <= my <= 450: current_cam = "CAM 2"
                    if 500 <= mx <= 600 and 470 <= my <= 520: current_cam = "CAM 3"

                # Click nút Bật/Tắt Hệ thống Camera (Nút lớn ở dưới cùng)
                if 300 <= mx <= 500 and 530 <= my <= 580:
                    camera_open = not camera_open

    # 2. XỬ LÝ LOGIC TRONG GAME
    if freddy_pos == 4:
        game_over = True

    # 3. VẼ GIAO DIỆN (RENDER)
    if not game_over and not win:
        if not camera_open:
            # --- MÀN HÌNH CHÍNH (VĂN PHÒNG BẢO VỆ) ---
            # Vẽ nền văn phòng (Thay đổi màu tùy thuộc vào Đèn)
            office_color = (30, 30, 30)
            if left_light and freddy_pos == 3:
                office_color = (150, 50, 50) # Hiện màu đỏ nếu Freddy ở cửa trái và bật đèn
            elif left_light or right_light:
                office_color = (80, 80, 80)
            pygame.draw.rect(screen, office_color, (120, 100, 560, 400))
            
            # Vẽ trạng thái Cửa
            if left_door: pygame.draw.rect(screen, RED, (120, 100, 30, 400))  # Cửa trái đóng
            if right_door: pygame.draw.rect(screen, RED, (650, 100, 30, 400)) # Cửa phải đóng

            # Vẽ các nút điều khiển bên Trái
            draw_button("DOOR", (20, 200, 80, 50), GREEN if left_door else GRAY)
            draw_button("LIGHT", (20, 270, 80, 50), YELLOW if left_light else GRAY)
            
            # Vẽ các nút điều khiển bên Phải
            draw_button("DOOR", (700, 200, 80, 50), GREEN if right_door else GRAY)
            draw_button("LIGHT", (700, 270, 80, 50), YELLOW if right_light else GRAY)
            
            # Gợi ý văn phòng
            txt = font.render("Chế độ văn phòng (Đang nhìn thẳng)", True, WHITE)
            screen.blit(txt, (260, 120))
            
        else:
            # --- MÀN HÌNH CAMERA ---
            pygame.draw.rect(screen, (10, 20, 10), (50, 50, 700, 450)) # Khung màn hình cam
            
            # Hiển thị nội dung dựa trên Camera được chọn và Vị trí của Freddy
            cam_info = f"Đang xem: {current_cam}"
            status_txt = "Phòng trống / Không thấy gì"
            
            if current_cam == "CAM 1":
                status_txt = "SÂN KHẤU: " + ("Freddy đang ở đây!" if freddy_pos == 1 else "Sân khấu trống trơn!")
            elif current_cam == "CAM 2":
                status_txt = "HÀNH LANG: " + ("Có bóng người đang tiến lại!" if freddy_pos == 2 else "Hành lang tối đen.")
            elif current_cam == "CAM 3":
                status_txt = "GẦN CỬA TRÁI: " + ("CẢNH BÁO: Hắn đang ở ngay ngoài cửa!" if freddy_pos == 3 else "Khu vực an toàn.")

            # Vẽ thông tin Camera lên màn hình
            screen.blit(font.render(cam_info, True, GREEN), (70, 70))
            screen.blit(font.render(status_txt, True, RED if "CẢNH BÁO" in status_txt else WHITE), (70, 110))
            
            # Vẽ các nút chuyển đổi Camera (Bản đồ thu nhỏ)
            draw_button("CAM 1", (500, 400, 100, 50), BLUE if current_cam == "CAM 1" else GRAY)
            draw_button("CAM 2", (620, 400, 100, 50), BLUE if current_cam == "CAM 2" else GRAY)
            draw_button("CAM 3", (500, 470, 100, 50), BLUE if current_cam == "CAM 3" else GRAY)

        # CẬP NHẬT HUD (Thông tin chung: Pin & Thời gian)
        draw_button("MỞ/TẮT CAMERA", (300, 530, 200, 50), BLUE if camera_open else GRAY)
        
        power_txt = font.render(f"Power: {round(power, 1)}%", True, GREEN if power > 30 else RED)
        time_txt = font.render(f"Time: {time_am} AM", True, WHITE)
        screen.blit(power_txt, (20, 20))
        screen.blit(time_txt, (680, 20))

    # --- MÀN HÌNH KẾT THÚC (THẮNG / THUA) ---
    elif game_over:
        screen.fill(BLACK)
        jumpscare_txt = large_font.render("FREDDY JUMPSCARE! GAME OVER", True, RED)
        screen.blit(jumpscare_txt, (SCREEN_WIDTH//2 - jumpscare_txt.get_width()//2, SCREEN_HEIGHT//2 - 50))
        
    elif win:
        screen.fill(BLACK)
        win_txt = large_font.render("6 AM - YOU WIN!", True, GREEN)
        screen.blit(win_txt, (SCREEN_WIDTH//2 - win_txt.get_width()//2, SCREEN_HEIGHT//2 - 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
