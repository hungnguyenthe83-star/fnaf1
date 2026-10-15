import pygame
import random
import sys

# Khởi tạo pygame
pygame.init()

# Cấu hình cửa sổ game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FNAF 1 Mini Remake - Python")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)
LIGHT_GRAY = (150, 150, 150)

# Cấu hình Fonts
font_large = pygame.font.SysFont("Arial", 40)
font_medium = pygame.font.SysFont("Arial", 25)
font_small = pygame.font.SysFont("Arial", 18)

# Trạng thái Game
power = 100.0  # Phần trăm pin
power_usage = 1  # Mức độ tiêu thụ điện cơ bản
door_left = False  # Trạng thái cửa trái (Đóng/Mở)
door_right = False  # Trạng thái cửa phải (Đóng/Mở)
camera_open = False  # Trạng thái màn hình camera
current_cam = "CAM 1A"  # Camera đang xem
game_over = False
victory = False

# Thời gian trong game
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()
time_survived = 0  # Tính bằng giây để quy đổi ra AM

# Danh sách phòng và mô tả vị trí của Freddy
# 1A: Sân khấu -> 1B: Khu ăn uống -> 2A: Hành lang trái -> Văn phòng (Tấn công nếu cửa mở)
freddy_pos = "CAM 1A"
freddy_move_timer = pygame.time.get_ticks()

def move_freddy():
    """Hệ thống tự động di chuyển AI Freddy dựa trên thời gian ngẫu nhiên"""
    global freddy_pos, game_over
    
    if freddy_pos == "CAM 1A":
        freddy_pos = "CAM 1B"
    elif freddy_pos == "CAM 1B":
        freddy_pos = "CAM 2A"
    elif freddy_pos == "CAM 2A":
        if door_left:
            # Nếu cửa trái đóng, Freddy bị chặn và quay về sân khấu
            freddy_pos = "CAM 1A"
        else:
            # Nếu cửa mở, người chơi bị jumpscare
            game_over = True

def draw_office():
    """Vẽ giao diện phòng làm việc của bảo vệ"""
    screen.fill(BLACK)
    
    # Vẽ góc nhìn phòng làm việc (Phông nền cơ bản)
    pygame.draw.rect(screen, GRAY, (100, 100, 600, 400))
    
    # Vẽ nút bấm và cửa bên trái
    color_door_l = GREEN if door_left else RED
    pygame.draw.rect(screen, color_door_l, (20, 250, 60, 100))
    txt_l = font_small.render("DOOR L", True, WHITE)
    screen.blit(txt_l, (25, 290))
    
    # Cửa vật lý bên trái (nếu đóng sẽ hiện tấm chắn che văn phòng)
    if door_left:
        pygame.draw.rect(screen, BLACK, (100, 100, 50, 400))
        
    # Vẽ nút bấm và cửa bên phải
    color_door_r = GREEN if door_right else RED
    pygame.draw.rect(screen, color_door_r, (720, 250, 60, 100))
    txt_r = font_small.render("DOOR R", True, WHITE)
    screen.blit(txt_r, (725, 290))
    
    # Cửa vật lý bên phải
    if door_right:
        pygame.draw.rect(screen, BLACK, (650, 100, 50, 400))

    # Cảnh báo nếu Freddy đang ở ngay sát hành lang trái (CAM 2A)
    if freddy_pos == "CAM 2A" and not door_left:
        warning_txt = font_large.render("CÓ TIẾNG BƯỚC CHÂN GẦN CỬA TRÁI!!!", True, RED)
        screen.blit(warning_txt, (120, 50))

def draw_cameras():
    """Vẽ giao diện hệ thống Camera an ninh"""
    screen.fill(BLACK)
    
    # Bản đồ mô phỏng nhà hàng
    pygame.draw.rect(screen, WHITE, (450, 250, 300, 250), 3)
    
    # Danh sách các nút Camera điều hướng
    cams = {
        "CAM 1A": (550, 280),
        "CAM 1B": (550, 360),
        "CAM 2A": (480, 450)
    }
    
    for cam_name, pos in cams.items():
        color = GREEN if current_cam == cam_name else LIGHT_GRAY
        pygame.draw.rect(screen, color, (pos[0], pos[1], 80, 40))
        cam_txt = font_small.render(cam_name, True, BLACK)
        screen.blit(cam_txt, (pos[0] + 10, pos[1] + 10))
        
    # Hiển thị hình ảnh giả lập khu vực camera đang quét
    pygame.draw.rect(screen, GRAY, (50, 80, 350, 400))
    cam_title = font_large.render(f"VIEWING: {current_cam}", True, WHITE)
    screen.blit(cam_title, (50, 30))
    
    # Hiển thị vị trí thực tế của Freddy trên camera ẩn/hiện
    if freddy_pos == current_cam:
        freddy_txt = font_large.render("[ ANIMATRONIC DETECTED ]", True, RED)
        screen.blit(freddy_txt, (60, 250))
    else:
        safe_txt = font_medium.render("Phòng trống...", True, GREEN)
        screen.blit(safe_txt, (70, 250))

def draw_hud(display_time):
    """Hiển thị các thông số sống còn: Pin, Thời gian, Nút bật Cam"""
    # Hiển thị số giờ sống sót (Mỗi 30 giây thực tế tăng 1 tiếng trong game, sống tới 6 AM là thắng)
    hour = int(display_time / 30) + 12
    if hour > 12:
        hour -= 12
    time_txt = font_large.render(f"{hour} AM", True, WHITE)
    screen.blit(time_txt, (700, 20))
    
    # Hiển thị lượng pin
    power_txt = font_medium.render(f"Power left: {int(power)}%", True, WHITE)
    screen.blit(power_txt, (20, 20))
    
    # Hiển thị mức tiêu thụ điện năng
    usage_str = ">" * power_usage
    usage_txt = font_small.render(f"Power usage: {usage_str}", True, GREEN if power_usage <= 2 else RED)
    screen.blit(usage_txt, (20, 50))
    
    # Nút bật/tắt thanh Camera dưới đáy màn hình
    pygame.draw.rect(screen, BLUE, (250, 530, 300, 40))
    cam_btn_txt = font_medium.render("BẬT / TẮT MONITOR (SPACE)", True, WHITE)
    screen.blit(cam_btn_txt, (260, 535))

# --- VÒNG LẶP CHÍNH CỦA TRÒ CHƠI ---
running = True
while running:
    # Tính toán thời gian
    current_ticks = pygame.time.get_ticks()
    seconds_passed = (current_ticks - start_ticks) / 1000
    
    # Xử lý sự kiện (Input)
    for event in pygame.event.get_events():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not victory:
            mx, my = pygame.mouse.get_pos()
            
            # Click chuột khi đang ở chế độ văn phòng (Màn hình thường)
            if not camera_open:
                # Nút Cửa Trái
                if 20 <= mx <= 80 and 250 <= my <= 350:
                    door_left = not door_left
                # Nút Cửa Phải
                if 720 <= mx <= 780 and 250 <= my <= 350:
                    door_right = not door_right
                    
            # Click chuột khi đang bật camera để đổi kênh quét
            else:
                if 550 <= mx <= 630 and 280 <= my <= 320: current_cam = "CAM 1A"
                if 550 <= mx <= 630 and 360 <= my <= 400: current_cam = "CAM 1B"
                if 480 <= mx <= 560 and 450 <= my <= 490: current_cam = "CAM 2A"
                
            # Click trực tiếp nút Monitor
            if 250 <= mx <= 550 and 530 <= my <= 570:
                camera_open = not camera_open

        if event.type == pygame.KEYDOWN:
            # Nhấn SPACE để đóng/mở Camera nhanh
            if event.key == pygame.K_SPACE and not game_over and not victory:
                camera_open = not camera_open

    # Tái thiết lập mức độ tiêu hao năng lượng dựa trên các thiết bị đang bật
    power_usage = 1 + int(door_left) + int(door_right) + int(camera_open)
    
    # Trừ thời lượng pin theo thời gian thực
    if not game_over and not victory:
        power -= (0.05 * power_usage)
        if power <= 0:
            power = 0
            game_over = True  # Hết pin = Tắt điện, Freddy lập tức jumpscare

    # Tính toán cơ chế di chuyển ngẫu nhiên của Robot cứ mỗi 7-12 giây
    if current_ticks - freddy_move_timer > random.randint(7000, 12000) and not game_over and not victory:
        move_freddy()
        freddy_move_timer = current_ticks

    # Điều kiện chiến thắng: Sống sót qua 180 giây (Tương đương sống tới 6 AM trong game)
    if seconds_passed >= 180 and not game_over:
        victory = True

    # --- KHOẢN VẼ ĐỒ HỌA LÊN MÀN HÌNH ---
    if game_over:
        screen.fill(BLACK)
        over_txt = font_large.render("GAME OVER - FREDDY JUMPSCARED YOU!", True, RED)
        screen.blit(over_txt, (80, 260))
    elif victory:
        screen.fill(BLACK)
        win_txt = font_large.render("6 AM - BẠN ĐÃ SỐNG SÓT THÀNH CÔNG!", True, GREEN)
        screen.blit(win_txt, (100, 260))
    else:
        # Cập nhật màn hình chính tùy theo trạng thái mở camera
        if camera_open:
            draw_cameras()
        else:
            draw_office()
            
        # Luôn luôn vẽ HUD thông số lên trên cùng
        draw_hud(seconds_passed)

    pygame.display.flip()
    clock.tick(30)  # Giới hạn 30 Khung hình / Giây
