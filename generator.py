from pynput import mouse
from tqdm import tqdm
import time
import sys

class RandomNumberCollector:
    def __init__(self, total_bytes):
        self.total_bytes = total_bytes
        self.random_numbers = []
        self.prev_time = time.time()
        self.file_name = f"{time.time()}.bin"
        self.pbar = tqdm(total=total_bytes, desc="Collecting random numbers", unit="byte")

    def on_move(self, x, y):
        current_time = time.time()
        time_diff = int((current_time - self.prev_time) * 1e6)  # 마이크로초 단위
        self.prev_time = current_time

        random_number = (x ^ y ^ time_diff) & 0xFF
        self.random_numbers.append(random_number)

        self.pbar.update(1)

        if len(self.random_numbers) >= self.total_bytes:
            self.save_random_numbers()
            self.pbar.close()
            return False

    def save_random_numbers(self):
        try:
            with open(self.file_name, 'wb') as f:
                f.write(bytearray(self.random_numbers))
            print(f"파일이 저장되었습니다: {self.file_name}")
        except IOError as e:
            print(f"파일 저장 중 에러 발생: {e}")

def main():
    try:
        total_bytes = int(input("생성할 난수파일 크기(바이트): "))
    except ValueError:
        print("정수만 입력가능합니다.")
        sys.exit()

    collector = RandomNumberCollector(total_bytes)
    print(f"마우스를 움직여 난수를 수집하세요. {total_bytes} 바이트의 난수가 모이면 자동으로 저장됩니다.")

    with mouse.Listener(on_move=collector.on_move) as listener:
        listener.join()

if __name__ == "__main__":
    main()
