import numpy as np
from PIL import Image
import os

def read_vcd(filename):
    """Lee el archivo VCD y devuelve una lista de eventos (timestamp, signal, value)."""
    events = []
    timestamp = 0
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                timestamp = int(line[1:])
            elif line.startswith(("0", "1")):
                value = int(line[0])
                signal = line[1]
                events.append((timestamp, signal, value))
    return events

def extract_line(events, start_idx, pixels_per_line, bit_duration):
    """Extrae los bits de una línea de vídeo a partir del índice de inicio."""
    line_start_time = events[start_idx][0]
    line_bits = np.zeros(pixels_per_line, dtype=np.uint8)

    # Valor inicial de D1
    current_value = 0
    j = start_idx - 1
    while j >= 0:
        if events[j][1] == '"':
            current_value = events[j][2]
            break
        j -= 1

    # Cambios futuros de D1
    next_changes = [(t, v) for t, s, v in events[start_idx:] if s == '"']
    next_idx = 0

    for p in range(pixels_per_line):
        sample_time = line_start_time + p * bit_duration
        while next_idx < len(next_changes) and next_changes[next_idx][0] <= sample_time:
            current_value = next_changes[next_idx][1]
            next_idx += 1
        line_bits[p] = current_value

    return line_bits

def decode_frames(events, pixels_per_line, active_lines, bit_duration, frame_duration_threshold):
    """Decodifica todos los frames de la lista eventos."""
    frames = []
    current_frame_lines = []
    last_sync_time = 0
    i = 0
    frame_count = 0

    while i < len(events):

        # Buscar el inicio de sincronización
        while i < len(events) and not (events[i][1] == "!" and events[i][2] == 1):
            i += 1
        if i >= len(events):
            break
        sync_start = events[i][0]

        # Nuevo frame si ha pasado suficiente tiempo
        if sync_start - last_sync_time > frame_duration_threshold and current_frame_lines:
            frame_array = np.array(current_frame_lines[:active_lines], dtype=np.uint8) * 255
            frames.append(Image.fromarray(frame_array, mode="L"))
            current_frame_lines = []
            frame_count += 1
            print(f"[+] Frame {frame_count} recuperado")

        last_sync_time = sync_start
        i += 1

        # Esperar fin del pulso de sincronización
        while i < len(events) and not (events[i][1] == "!" and events[i][2] == 0):
            i += 1
        if i >= len(events):
            break

        # Extraer línea de video
        line_bits = extract_line(events, i, pixels_per_line, bit_duration)
        current_frame_lines.append(line_bits)
        i += 1

    # Guardar último frame
    if current_frame_lines:
        frame_array = np.array(current_frame_lines[:active_lines], dtype=np.uint8) * 255
        frames.append(Image.fromarray(frame_array, mode="L"))
        frame_count += 1
        print(f"[+] Frame {frame_count} recuperado")

    return frames

def save_frames(frames, folder="frames", prefix="frame"):
    """Guarda los frames como imágenes en formato png"""
    os.makedirs(folder, exist_ok=True)
    
    for i, frame in enumerate(frames):
        filename = os.path.join(folder, f"{prefix}_{i:04d}.png")
        frame.save(filename)
    
    print(f"\n[!] Guardados {len(frames)} frames en '{folder}/'")

def main():

        # Configuración
        pixels_per_line = 768
        active_lines = 576
        bit_duration = 250  # ns
        sync_pulse_duration = 4000  # ns
        frame_duration_threshold = 1_000_000  # ns

        events = read_vcd("video_capture.vcd")
        frames = decode_frames(events, pixels_per_line, active_lines, bit_duration, frame_duration_threshold)
        if frames:
            save_frames(frames)
        else:
            print("No se detectaron frames.")

if __name__ == "__main__":
    main()