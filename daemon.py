import atexit
import os
import sys
import time
from abc import ABC, abstractmethod
from signal import SIGTERM


class Daemon(ABC):
    """
    Класс родитель, позволяющий выполнить демонизацию задачи.

    Для демонизации необходимо создать класс наследник класса Daemon и желаемую задачу для демонизации
    поместить в метод daemon.
    """

    def __init__(self, pid_file, stdout='/dev/null', stderr='/dev/null'):

        self.pid_file = pid_file
        self.stderr = stderr
        self.stdout = stdout
        self.START_MASSAGE = 'Started with pid:'

    @abstractmethod
    def daemon(self):
        """Метод который будет демонизирован."""
        pass

    @staticmethod
    def new_fork():
        """Метод создает компию основного процесса и завершает основной процесс."""
        try:
            middle_pid = os.fork()
            if middle_pid > 0:
                # выходим из основного потока (делаем дочерний процесс сиротой)
                sys.exit(0)
        except OSError as e:
            sys.stderr.write(f"fork error: {e.errno} - {e.strerror}")
            sys.exit(1)

    def daemonize(self):
        """Метод производящий дублирование потока с помощью fork и уводящий его в фон (демонизирует)."""
        self.new_fork()

        # производится отеление процесса от родителя и его полная демонизация
        # https://stackoverflow.com/questions/45911705/why-use-os-setsid-in-python - подробное описание или смотри
        # README пункт "Выведение потока в фон"
        os.chdir('/')  # установка процесса в корень
        os.setsid()  # создание сеанса и выставление процесса лидером группы

        self.new_fork()
        daemon_pid = str(os.getpid())

        print(f"{self.START_MASSAGE} {daemon_pid}")

        with open(self.pid_file, 'w') as file:
            file.write(daemon_pid)

        # модуль следит за тем чтобы перед завершением программы файл с pid был удален
        atexit.register(self.del_pid_file)

        # перенаправление стандартных выводов в файл

        # открываем файлы которые будут использоваться для стандартных выводов
        system_output = open(self.stdout, 'a+')
        system_error = open(self.stderr, 'a+')

        # устанавливаем дескрипторы стандартных выводов на файлы
        os.dup2(system_output.fileno(), sys.stdout.fileno())
        os.dup2(system_error.fileno(), sys.stderr.fileno())

        system_output.close()
        system_error.close()

    def del_pid_file(self):
        """Метод для удаления файла с PID."""
        try:
            os.remove(self.pid_file)
        except OSError:
            pass

    def start(self):
        """Метод производит запуск демонизацию метода daemon."""
        pid = self.get_pid()
        if pid:
            print(f'File with pid already exist. Daemon already running.\nCheck {self.pid_file}')
            sys.exit(1)
        self.daemonize()
        self.daemon()

    def stop(self):
        """Метод производит остановку демона."""
        pid = self.get_pid()
        if pid is None:
            print(f'Pid file does not exist\nCheck it {self.pid_file}')
            sys.exit(1)
        # убийство демона
        try:
            while True:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError as e:
            if "No such process" not in e.strerror or "Нет такого процесса" not in e.strerror:
                if os.path.exists(self.pid_file):
                    self.del_pid_file()
            else:
                print(e.strerror)
                sys.exit(1)

    def restart(self):
        """Метод для перезапуска демона."""
        self.stop()
        time.sleep(0.1)
        self.start()

    def get_pid(self) -> None or int:
        """Возвращает pid или None если не вышло его достать."""
        try:
            with open(self.pid_file, 'r') as file:
                pid = int(file.readline())
        except IOError:
            pid = None
        except ValueError:
            print('Pid file is broken')
            sys.exit(1)
        return pid
