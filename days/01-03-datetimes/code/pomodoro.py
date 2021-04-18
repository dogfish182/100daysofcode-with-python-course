#!/usr/bin/env python
from datetime import datetime, timedelta
from time import sleep
import typer
import sys

app = typer.Typer()


class Pommy:

    min_to_day_multiplier = 0.00069444444444444

    def __init__(self, work_time: int, short_break: int, long_break: int) -> None:
        self._work_time = timedelta(float(work_time*Pommy.min_to_day_multiplier))
        self._short_break = timedelta(float(short_break*Pommy.min_to_day_multiplier))
        self._long_break = timedelta(float(long_break*Pommy.min_to_day_multiplier))
        self.phases = {'work': self._work_time,
                       'short_break': self._short_break,
                        'long_break': self._long_break}
        self.current_phase = ''
        self.short_break_count = 0

    @property
    def work_time(self) -> timedelta:
        return self._work_time

    @work_time.setter
    def work_time(self, new_value: str) -> None:
        self._work_time = timedelta(float(new_value))

    @property
    def short_break(self) -> timedelta:
        return self._short_break

    @short_break.setter
    def short_break(self, new_value: str) -> None:
        self._short_break = timedelta(float(new_value))

    @property
    def long_break(self) -> timedelta:
        return self._long_break

    @long_break.setter
    def long_break(self, new_value: str) -> None:
        self._long_break = timedelta(float(new_value))

    def get_next_phase(self):
        if not self.current_phase:
            self.current_phase = 'work'
            return self.current_phase
        elif self.current_phase == 'short_break':
            self.current_phase = 'work'
            return self.current_phase
        if self.current_phase == 'work' and self.short_break_count < 3:
            self.short_break_count = self.short_break_count + 1
            self.current_phase = 'short_break'
            return 'short_break'
        self.short_break_count = 0
        return 'long_break'

    def run_phase(self, phase: str):
        time_start = datetime.now()
        time_end = time_start + self.phases.get(phase)
        while time_start + self.phases.get(self.current_phase) > datetime.now():
            print(
                f'time of start is {time_start} current phase is {self.current_phase} '
                f'phase will end at in {time_end - datetime.now()} seconds at {time_end}')
            sleep(2)

    def start(self):
        while True:
            next_phase = self.get_next_phase()
            self.run_phase(next_phase)


@app.command()
def timer(work_time: str, short_break: str, long_break: str):
    try:
        work_time = int(work_time)
        short_break = int(short_break)
        long_break = int(long_break)
    except ValueError:
        print('Please enter your timer varibles in whole minutes only')
        sys.exit(1)
    timer = Pommy(work_time, short_break, long_break)
    timer.start()


if __name__ == '__main__':
    app()
