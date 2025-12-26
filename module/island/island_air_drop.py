from module.island.island import *
from time import sleep

class IslandDailyGather(Island):
    def run(self):
        now = datetime.now()
        next_daily_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        next_daily_time += timedelta(days=1)
        self.goto_postmanage()
        if self.appear_then_click(MY_AIR_DROP_ALREADY):
            self.ui_goto(page_island)
            self.island_air_drop()
            #self.appear_then_click(skip)
            self.island_down(1000)
            self.island_air_drop()
        self.ui_goto(page_island_management)
        self.steal_air_drop()
        self.ui_goto(page_island_visit)
        image = self.device.screenshot()
        ocr_air_drop = Digit(OCR_AIR_DROP, name='air_drop', letter=(170, 170, 170), threshold=80,
                                    alphabet='0123456789')
        number = ocr_air_drop.ocr(image)
        if number>0:
            next_run_time = now + timedelta(hours=5)
            self.config.task_delay(target=next_run_time)
        else:
            self.config.task_delay(target=next_daily_time)
    def steal_air_drop(self):
        self.ui_goto(page_island_visit)
        image = self.device.screenshot()
        ocr_air_drop = Digit(OCR_AIR_DROP, name='air_drop', letter=(170, 170, 170), threshold=80,
                                    alphabet='0123456789')
        number = ocr_air_drop.ocr(image)
        times = 5
        while number > 0:
            while times > 0:
                self.device.screenshot()
                self.appear_then_click(ONES_AIR_DROP,offset=300)
                if self.island_access_map_check():
                    self.post_manage_up_swipe(450)
                else:
                    while True:
                        self.device.screenshot()
                        if self.appear_then_click(ISLAND_ACCESS_MAP):
                            continue
                        if self.appear(ISLAND_MAP_CHECK):
                            self.device.click(ISLAND_MAP_GOTO_ISLAND)
                            break
                        self.device.sleep(1)
                    self.run_and_get()
                    self.device.click(AIR_DROP_RUN_AWAY)
                times -= 1
                number -= 1

    def island_access_map_check(self):
        while True:
            self.device.screenshot()
            if self.appear(ISLAND_ACCESS_MAP):
                return False
            if self.appear(CANT_ACCESS):
                return True

    def island_air_drop(self):
        self.device.click(ISLAND_AIR_DROP_A)
        sleep(0.1)
        self.device.click(ISLAND_AIR_DROP_B)
        sleep(0.1)
        self.device.click(ISLAND_AIR_DROP_C)
        sleep(0.5)
        self.device.click(ISLAND_AIR_DROP_A)
        sleep(0.1)
        self.device.click(ISLAND_AIR_DROP_B)
        sleep(0.1)
        self.device.click(ISLAND_AIR_DROP_C)
    def run_and_get(self):
        self.island_up(3000)
        self.island_right(700)
        self.island_up(2000)
        self.device.click(ISLAND_JUMP)
        self.island_up(1200)
        self.island_right(2000)
        self.island_up(6500)
        self.island_right(1000)
        self.island_up(2300)
        self.island_right(2000)
        self.island_up(4000)
        self.island_right(2600)
        self.island_up(300)
        self.device.click(ISLAND_JUMP)
        self.island_up(1300)
        self.island_air_drop()
        for _ in range(1):
            self.device.screenshot()
            if self.appear(ISLAND_AIR_DROP_ALREADY_GETTED, offset=200):
                break
            self.island_up(500)
            self.island_air_drop()
            self.device.screenshot()
            if self.appear(ISLAND_AIR_DROP_ALREADY_GETTED, offset=200):
                break
            self.island_right(500)
            self.island_air_drop()
            self.device.screenshot()
            if self.appear(ISLAND_AIR_DROP_ALREADY_GETTED, offset=200):
                break
            self.island_down(500)
            self.island_air_drop()



if __name__ == "__main__":
    az =IslandDailyGather('alas', task='Alas')
    az.device.screenshot()
    az.run()