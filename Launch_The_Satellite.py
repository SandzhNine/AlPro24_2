import pygame
import numpy as np
import csv
import textwrap
from datetime import datetime
import sys

pygame.init()
#Resolution 4:5 Ratio
WW = 540
WH = 675

screen = pygame.display.set_mode((WW, WH))
pygame.display.set_caption("Launch the Satellite")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TURQUOISE = (64, 224, 208)

#pygame.mixer.music.load("Music/background_music2.mp3") 
#pygame.mixer.music.play(-1, 0.0)

gameBG = pygame.image.load("Image/BG0.png")
history = pygame.image.load("Image/History.png")
intruksi = pygame.image.load("Image/Intruksi.png")
#Button Import
play_unp = pygame.image.load("Image/Play Button.png")
play_prs = pygame.image.load("Image/Play Button (Pressed).png")
htp_unp = pygame.image.load("Image/HTP Button.png")
htp_prs = pygame.image.load("Image/HTP Button (Pressed).png")
quit_unp = pygame.image.load("Image/Quit Button.png")
quit_prs = pygame.image.load("Image/Quit Button (Pressed).png")
back_button_img = pygame.image.load("Image/Back.png")
history_button_img = pygame.image.load("Image/Hstr.png")
delete_button_img = pygame.image.load("Image/Delete.png")

warning_img = pygame.image.load("Image/warning.png")
play_img = pygame.image.load("Image/play.png")
input_png = pygame.image.load("Image/input.png")

earth_img = pygame.image.load("Image/earth.png")
satellite_img = pygame.image.load("Image/satellite.png")
background_img = pygame.image.load("Image/background.png")

gameBG = pygame.transform.scale(gameBG, (WW, WH))
history = pygame.transform.scale(history, (WW, WH))
intruksi = pygame.transform.scale(intruksi, (WW, WH))

earth_img = pygame.transform.scale(earth_img, (200, 200))
satellite_img = pygame.transform.scale(satellite_img, (50, 50))
background_img = pygame.transform.scale(background_img, (WW, WH))

def resize_button(image, target_width=250, target_height=90):
    return pygame.transform.scale(image, (target_width, target_height))

def center_align(image_width, image_height, offset_y=0):
    x = (WW - image_width) // 2
    y = (WH - image_height) // 2 + offset_y
    return x, y

def resize_image(image, max_width, max_height):
    width, height = image.get_size()
    aspect_ratio = width / height
    
    if width > height:
        new_width = min(max_width, width)
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = min(max_height, height)
        new_width = int(new_height * aspect_ratio)
    
    return pygame.transform.scale(image, (new_width, new_height))

play_unp = resize_button(play_unp)
play_prs = resize_button(play_prs)
htp_unp = resize_button(htp_unp)
htp_prs = resize_button(htp_prs)
quit_unp = resize_button(quit_unp)
quit_prs = resize_button(quit_prs)

warning_img = resize_image(warning_img, WW // 2, WH // 3)
play_img = resize_image(play_img, WW // 2, WH // 3)
input_png = resize_image(input_png, WW // 2, WH // 3)

button_gap = 20
play_x, play_y = center_align(play_unp.get_width(), play_unp.get_height(), 20)
htp_x, htp_y = center_align(htp_unp.get_width(), htp_unp.get_height(), 110)
quit_x, quit_y = center_align(quit_unp.get_width(), quit_unp.get_height(), 200)

font = pygame.font.Font("font/8bit.TTF", 48)
input_box = pygame.Rect(WW // 2 - 100, WH // 2 - 50, 200, 50)
active = False
text = ''
color_inactive = pygame.Color(TURQUOISE)
color_active = pygame.Color(WHITE)
color = color_inactive
text_surface = font.render(text, True, WHITE)
clock = pygame.time.Clock()

def log_input_to_csv(vs):
    v0 = calculate_orbit_velocity()
    # Mendapatkan informasi tanggal dan waktu
    current_time = datetime.now()
    date = current_time.strftime("%Y-%m-%d")
    time = current_time.strftime("%H:%M:%S")
    try:
        inputv = int(vs) 
        if 1 <= inputv <= 99999:
            if inputv == v0:
                keterangan = "Success"
            elif v0 < inputv <= 99999:
                keterangan = "Fly Away"
            elif 0 < inputv < v0:
                keterangan = "Crash"
            else:
                keterangan = "Invalid"  # Jika nilai diluar rentang 1-10
        else:
            keterangan = "Invalid"  # Jika input diluar rentang 1-10
    except ValueError:
        keterangan = "Invalid"

    # Membuka file CSV dalam mode append (Menambahkan Data)
    with open('input_log.csv', mode='a', newline='') as file:
        fieldnames = ["Tanggal", "Waktu", "Input", "Keterangan"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader() # Label tabel
        
        # Menulis data log ke CSV
        writer.writerow({
            "Tanggal": date,
            "Waktu": time,
            "Input": vs,
            "Keterangan": keterangan
        })

def clear_history():
    with open('input_log.csv', 'w', newline='') as file:
        file.write("Tanggal,Waktu,Input,Keterangan\n")

def draw_input_box():
    pygame.draw.rect(screen, color, input_box, 2) 
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5)) 

def get_input():
    global text, active, color, text_surface, v
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = True
                color = color_active
            else:
                active = False
                color = color_inactive

        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    try:
                        v = int(text)
                        log_input_to_csv(v)
                        return v
                    except ValueError:
                        log_input_to_csv(text)
                        text = ''
                        screen.blit(warning_img, (WW // 2 - warning_img.get_width() // 2, 400))
                        pygame.display.update()
                        pygame.time.wait(1000)
                        continue
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif len(text) < 5:
                    text += event.unicode
                text_surface = font.render(text, True, WHITE)
    return None

#Button Function
def buttonfunction(x, y, bs, bt):
    if bt == "play":
        button = play_prs if bs else play_unp
    elif bt == "htp":
        button = htp_prs if bs else htp_unp
    elif bt == "quit":
        button = quit_prs if bs else quit_unp
    screen.blit(button, (x, y))

def backbutton():
    back_button_img_resized = resize_image(back_button_img, 200, 100)
    backbutton_width = back_button_img_resized.get_width()
    backbutton_height = back_button_img_resized.get_height()

    x_axis, y_axis = 55, 15
    backbutton_x = WW - backbutton_width - 12.5 + x_axis
    backbutton_y = WH - backbutton_height - 12.5 + y_axis

    screen.blit(back_button_img_resized, (backbutton_x, backbutton_y))

    return backbutton_x, backbutton_y, backbutton_width, backbutton_height

def read_log_history():
    log_entries = []
    try:
        with open('input_log.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader) #Skip baris header label
            for row in reader:
                log_entries.append(row)
    except FileNotFoundError:
        print("File not found.")
    return log_entries

def display_history():
    screen.fill(WHITE) 
    screen.blit(history, (0, 0))  
    log_entries = read_log_history() 
    
    if not log_entries:
        font = pygame.font.Font("font/8bit.TTF", 20)
        text = font.render("No input history available", True, WHITE)
        screen.blit(text, (WW // 2 - text.get_width() // 2, WH // 2)) 
        pygame.display.update()
        pygame.time.wait(2000)  
        play() 

    font = pygame.font.Font("font/8bit.TTF", 15) 
    y_offset = 200 
    for entry in log_entries:
        date, time, vs, keterangan = entry
        log_text = f"{date} {time} | {vs} | {keterangan}"
        wrapped_text = textwrap.wrap(log_text, width=90)
        for line in wrapped_text:
            entry_text = font.render(line, True, WHITE)
            screen.blit(entry_text, (WW // 2 - entry_text.get_width() // 2, y_offset))
            y_offset += 25  

    pygame.display.update()  
    pygame.time.wait(5000)  # Tampilkan history selama (delay) 5 detik

def history_button():
    history_button_img_resized = resize_image(history_button_img, 200, 50) 
    history_button_width = history_button_img_resized.get_width()
    history_button_height = history_button_img_resized.get_height()

    history_button_x = (WW - history_button_width) // 2
    history_button_y = WH - history_button_height - 175 

    screen.blit(history_button_img_resized, (history_button_x, history_button_y))

    return history_button_x, history_button_y, history_button_width, history_button_height

def clear_button():
    clear_button_img_resized = resize_image(delete_button_img, 200, 50)
    clear_button_x = (WW - clear_button_img_resized.get_width()) // 2
    clear_button_y = WH - clear_button_img_resized.get_height() - 100
    screen.blit(clear_button_img_resized, (clear_button_x, clear_button_y))
    return clear_button_x, clear_button_y, clear_button_img_resized.get_width(), clear_button_img_resized.get_height()

def play():
    v = None
    while True:
        screen.fill(WHITE)
        screen.blit(gameBG, (0, 0))
        screen.blit(play_img, (WW // 2 - play_img.get_width() // 2, 250))
        screen.blit(input_png, (WW // 2 - input_png.get_width() // 2, 321))
        draw_input_box()
        input_box.y = 350

        v = get_input()

        if v is not None:
            v = int(v)
            if v < 1 or v > 99999:
                screen.blit(warning_img, (WW // 2 - warning_img.get_width() // 2, 400))
                pygame.display.update()
                pygame.time.wait(1000)
                continue
            else:
                break

        backbutton_x, backbutton_y, backbutton_w, backbutton_h = backbutton()
        history_button_x, history_button_y, history_button_w, history_button_h = history_button()
        clear_button_x, clear_button_y, clear_button_w, clear_button_h = clear_button()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if backbutton_x <= event.pos[0] <= backbutton_x + backbutton_w and \
                   backbutton_y <= event.pos[1] <= backbutton_y + backbutton_h:
                    main_menu()
                elif history_button_x <= event.pos[0] <= history_button_x + history_button_w and \
                     history_button_y <= event.pos[1] <= history_button_y + history_button_h:
                    display_history()
                elif clear_button_x <= event.pos[0] <= clear_button_x + clear_button_w and \
                     clear_button_y <= event.pos[1] <= clear_button_y + clear_button_h:
                    clear_history()

        pygame.display.flip()

    if v is not None and 1 <= v <= 99999:
        animasi(v)

def menu_htp(image_path):
    run = True
    while run:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                backbuttonx, backbuttony, backbutton_w, backbutton_h = backbutton()
                if backbuttonx <= event.pos[0] <= backbuttonx + backbutton_w and backbuttony <= event.pos[1] <= backbuttony + backbutton_h:
                    return
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (WW, WH))
        screen.blit(image, (0, 0))
        backbutton()
        pygame.display.flip()
    pygame.quit()

def main_menu():
    run = True
    bs = {"play": False, "htp": False, "quit": False}

    while run:
        screen.blit(gameBG, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_x <= event.pos[0] <= play_x + play_unp.get_width() and \
                   play_y <= event.pos[1] <= play_y + play_unp.get_height():
                    bs["play"] = True
                elif htp_x <= event.pos[0] <= htp_x + htp_unp.get_width() and \
                     htp_y <= event.pos[1] <= htp_y + htp_unp.get_height():
                    bs["htp"] = True
                elif quit_x <= event.pos[0] <= quit_x + quit_unp.get_width() and \
                     quit_y <= event.pos[1] <= quit_y + quit_unp.get_height():
                    bs["quit"] = True
            if event.type == pygame.MOUSEBUTTONUP:
                if play_x <= event.pos[0] <= play_x + play_unp.get_width() and \
                   play_y <= event.pos[1] <= play_y + play_unp.get_height():
                    if bs["play"]:
                        play()
                        bs["play"] = False
                elif htp_x <= event.pos[0] <= htp_x + htp_unp.get_width() and \
                     htp_y <= event.pos[1] <= htp_y + htp_unp.get_height():
                    if bs["htp"]:
                        menu_htp("Image/Htp.png")
                        bs["htp"] = False
                elif quit_x <= event.pos[0] <= quit_x + quit_unp.get_width() and \
                     quit_y <= event.pos[1] <= quit_y + quit_unp.get_height():
                    if bs["quit"]:
                        run = False
        buttonfunction(play_x, play_y, bs["play"], "play")
        buttonfunction(htp_x, htp_y, bs["htp"], "htp")
        buttonfunction(quit_x, quit_y, bs["quit"], "quit")

        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

def baca_konstanta(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        constants = next(reader)
        G = float(constants['G'])
        M = float(constants['M'])
        R_earth = float(constants['R_earth'])
        h_orbit = float(constants['h_orbit'])
    return G, M, R_earth, h_orbit

def calculate_orbit_velocity(csv_file='Konstanta Game.csv'):
    G, M, R_earth, h_orbit = baca_konstanta(csv_file)
    r = R_earth + h_orbit 
    
    # Menghitung kecepatan orbit (m/s)
    v_orbit = np.sqrt(G * M / r)
    
    # Mengonversi kecepatan ke km/jam
    v_orbit_kmh = v_orbit * 3.6  # m/s ke km/h
    v0 = round(v_orbit_kmh)
    
    return v0

def orbit():
    # Jalur Spiral
    spiral = np.linspace(0, 2 * np.pi, 150)  
    radius_spiral = np.linspace(1, 2, 150) 
    x_spiral = radius_spiral * np.cos(spiral) 
    y_spiral = radius_spiral * -np.sin(spiral)  

    # Jalur Lingkaran (Orbit)
    orbit = np.linspace(0, 4 * np.pi, 300)  
    radius_orbit = 2  
    x_orbit = radius_orbit * np.cos(orbit) 
    y_orbit = radius_orbit * -np.sin(orbit)

    x = np.concatenate((x_spiral, x_orbit))
    y = np.concatenate((y_spiral, y_orbit))

    return x, y

def orbitgagal():
    # Jalur Spiral Meluncur
    theta_out = np.linspace(0, 2*np.pi, 150) 
    radius_out = np.linspace(1, 2, 150)  
    x_out = radius_out * np.cos(theta_out) 
    y_out = radius_out * -np.sin(theta_out)  

    # Jalur Spiral Jatuh
    theta_in = np.linspace(2*np.pi, 0, 150)  
    radius_in = np.linspace(2, 1, 150)  
    x_in = radius_in * np.cos(theta_in)  
    y_in = radius_in * np.sin(theta_in) 

    x = np.concatenate((x_out, x_in))
    y = np.concatenate((y_out, y_in))

    return x, y

def orbitover():
    # Jalur Spiral
    spiral = np.linspace(0, 2 * np.pi, 150) 
    radius_spiral = np.linspace(1, 3, 150)  
    x_spiral = radius_spiral * np.cos(spiral) 
    y_spiral = radius_spiral * -np.sin(spiral)  

    #Jalur lurus terbang bebas
    x_straight_start = x_spiral[-1]
    y_straight_start = y_spiral[-1]

    panjang_lintasan = 50  
    angle = np.pi / -2  
    x_straight = x_straight_start + np.linspace(0, panjang_lintasan * np.cos(angle), 150)
    y_straight = y_straight_start + np.linspace(0, panjang_lintasan * np.sin(angle), 150)

    x = np.concatenate((x_spiral, x_straight))
    y = np.concatenate((y_spiral, y_straight))

    return x, y

def animasi(v):
    v0 = calculate_orbit_velocity()
    if v == v0:
        x, y = orbit()
    elif v >= v0:
        x, y = orbitover()
    elif v <= v0:
        x, y = orbitgagal()

    screen = pygame.display.set_mode((WW, WH))
    earth_pos = (WW // 2 - earth_img.get_width() // 2, WH // 2 - earth_img.get_height() // 2)

    clock = pygame.time.Clock()
    frame = 0

    while frame < len(x):
        screen.fill(BLACK)  # Clear screen with black
        # Draw background
        screen.blit(background_img, (0, 0))
        # Draw Earth
        screen.blit(earth_img, earth_pos)
        # Draw the red orbit path
        for i in range(frame + 1):
            pygame.draw.circle(screen, (255, 0, 0), 
                               (int(WW / 2 + x[i] * 100), int(WH / 2 + y[i] * 100)), 2)
        # Draw satellite 
        satellite_pos = (WW / 2 + x[frame] * 100 - satellite_img.get_width() // 2,
                         WH / 2 + y[frame] * 100 - satellite_img.get_height() // 2)
        screen.blit(satellite_img, satellite_pos)
        pygame.display.flip()

        # FPS cuyyyyy
        if v == v0:
            fps = 30
        elif v <= v0:
            fps = 15
        elif v >= v0:
            fps = 60
        clock.tick(fps)  # 60 FPS
        frame += 1

        #Biar bisa di close x
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    play()
    
main_menu()