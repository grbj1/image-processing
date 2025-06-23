import os
import cv2
import numpy as np


class ConsoleImageProcessor:
    def __init__(self):
        self.image = None
        self.original_image = None
        self.log_file = "image_processing_log.txt"

        # Очищаем или создаем лог-файл
        with open(self.log_file, 'w') as f:
            f.write("=== Image Processing Log ===\n")

        self.log("Программа запущена. Добро пожаловать в консольный обработчик изображений!")

    def log(self, message):
        """Записывает сообщение в лог-файл и выводит в консоль"""
        print(message)
        with open(self.log_file, 'a') as f:
            f.write(message + "\n")

    def load_image_from_file(self):
        """Загрузка изображения с диска"""
        while True:
            file_path = input("Введите путь к изображению: ").strip('"\' ')
            file_path = os.path.normpath(file_path)

            if not os.path.exists(file_path):
                self.log(f"Ошибка: Файл '{file_path}' не найден!")
                continue

            self.image = cv2.imread(file_path)
            if self.image is not None:
                self.original_image = self.image.copy()
                self.log(f"Изображение успешно загружено. Размер: {self.image.shape[1]}x{self.image.shape[0]}")
                return True
            else:
                self.log("Ошибка: Не удалось загрузить изображение. Проверьте формат файла.")
                return False

    def capture_image_from_camera(self):
        """Захват изображения с веб-камеры"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.log("Ошибка: Веб-камера не найдена!")
            return False

        self.log("Нажмите любую клавишу для захвата изображения...")
        ret, frame = cap.read()
        if ret:
            self.image = frame
            self.original_image = self.image.copy()
            self.log(f"Изображение с камеры захвачено. Размер: {self.image.shape[1]}x{self.image.shape[0]}")
            cap.release()
            return True
        else:
            self.log("Ошибка при захвате изображения с камеры!")
            cap.release()
            return False

    def get_initial_image(self):
        """Получение начального изображения (с диска или камеры)"""
        self.log("\n=== Источник изображения ===")
        self.log("1. Загрузить из файла")
        self.log("2. Сделать снимок с камеры")
        self.log("3. Выход")

        while True:
            try:
                choice = int(input("Выберите источник изображения (1-3): "))
                if choice == 1:
                    return self.load_image_from_file()
                elif choice == 2:
                    return self.capture_image_from_camera()
                elif choice == 3:
                    self.log("Завершение работы программы...")
                    return False
                else:
                    self.log("Неверный выбор! Попробуйте снова.")
            except ValueError:
                self.log("Ошибка: введите число от 1 до 3!")

    def save_image(self):
        """Сохранение текущего изображения"""
        if self.image is None:
            self.log("Нет изображения для сохранения!")
            return

        file_path = input("Введите путь для сохранения (по умолчанию output.jpg): ").strip('"\' ') or "output.jpg"
        file_path = os.path.normpath(file_path)

        try:
            cv2.imwrite(file_path, self.image)
            self.log(f"Изображение успешно сохранено как {file_path}")
        except Exception as e:
            self.log(f"Ошибка при сохранении: {str(e)}")

    def show_channel(self):
        """Отображение выбранного цветового канала"""
        channel = input("Выберите канал (R, G, B): ").upper()
        if channel not in ['R', 'G', 'B']:
            self.log("Неверный выбор канала!")
            return

        ch_index = {'B': 0, 'G': 1, 'R': 2}[channel]
        zeros = np.zeros_like(self.image)
        zeros[:, :, ch_index] = self.image[:, :, ch_index]

        cv2.imshow(f"{channel} Channel", zeros)
        self.log(f"Отображен {channel}-канал. Нажмите любую клавишу чтобы продолжить...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def apply_averaging(self):
        """Применение усредняющего фильтра"""
        while True:
            try:
                ksize = int(input("Введите размер ядра (нечетное число >=3): "))
                if ksize >= 3 and ksize % 2 == 1:
                    break
                self.log("Размер ядра должен быть нечетным числом >=3!")
            except ValueError:
                self.log("Ошибка: Введите целое число!")

        blurred = cv2.blur(self.image, (ksize, ksize))
        self.image = blurred
        self.log(f"Применен усредняющий фильтр с ядром {ksize}x{ksize}")

        cv2.imshow("Averaged Image", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def grayscale(self):
        """Преобразование в оттенки серого"""
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        self.log("Изображение преобразовано в оттенки серого")

        cv2.imshow("Grayscale Image", gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def draw_rectangle(self):
        """Рисование прямоугольника на изображении"""
        try:
            x1 = int(input("X верхнего левого угла: "))
            y1 = int(input("Y верхнего левого угла: "))
            x2 = int(input("X нижнего правого угла: "))
            y2 = int(input("Y нижнего правого угла: "))

            img_copy = self.image.copy()
            cv2.rectangle(img_copy, (x1, y1), (x2, y2), (255, 0, 0), 2)
            self.image = img_copy
            self.log(f"Нарисован прямоугольник с координатами ({x1},{y1})-({x2},{y2})")

            cv2.imshow("Image with Rectangle", self.image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except ValueError:
            self.log("Ошибка: координаты должны быть целыми числами!")

    def reset_image(self):
        """Сброс к оригинальному изображению"""
        self.image = self.original_image.copy()
        self.log("Изображение сброшено к оригиналу")

    def show_processing_menu(self):
        """Отображение меню обработки изображения"""
        self.log("\n=== Меню обработки ===")
        self.log("1. Показать цветовой канал (R/G/B)")
        self.log("2. Применить усредняющий фильтр")
        self.log("3. Преобразовать в оттенки серого")
        self.log("4. Нарисовать прямоугольник")
        self.log("5. Сохранить текущее изображение")
        self.log("6. Сбросить изменения")
        self.log("7. Выход")

        try:
            choice = int(input("Выберите действие (1-7): "))
            return choice
        except ValueError:
            self.log("Ошибка: введите число от 1 до 7!")
            return None

    def run(self):
        """Основной цикл программы"""
        if not self.get_initial_image():
            return

        while True:
            choice = self.show_processing_menu()

            if choice == 1:
                self.show_channel()
            elif choice == 2:
                self.apply_averaging()
            elif choice == 3:
                self.grayscale()
            elif choice == 4:
                self.draw_rectangle()
            elif choice == 5:
                self.save_image()
            elif choice == 6:
                self.reset_image()
            elif choice == 7:
                self.log("Завершение работы программы...")
                break
            else:
                if choice is not None:
                    self.log("Неверный выбор! Попробуйте снова.")


if __name__ == "__main__":
    processor = ConsoleImageProcessor()
    processor.run()