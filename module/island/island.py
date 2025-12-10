from module.island.assets import *
from module.ui.ui import UI
from module.ui.page import *
from module.base.timer import Timer
from module.handler.info_handler import InfoHandler
from module.ocr.ocr import *
from datetime import datetime



class Island(UI, InfoHandler,Timer):
    def goto_management(self):
        self.ui_goto(page_island)
        while True:
            self.device.screenshot()
            if self.appear(ISLAND_CHECK):
                self.device.click(ISLAND_GOTO_MANAGEMENT)
            if self.appear(ISLAND_MANAGEMENT_CHECK):
                break
    def goto_island_map(self):
        self.ui_goto(page_island)
        while True:
            self.device.screenshot()
            if self.appear_then_click(ISLAND_GOTO_MAP):
                continue
            if self.appear(ISLAND_MAP_CHECK):
                break


    def island_map_goto(self,destination):
        button_map = {
            'mine_forest': {
                'click': ISLAND_MAP_MINE_FOREST,
                'check': ISLAND_MAP_MINE_FOREST_CHECK
            },
            'farm': {
                'click': ISLAND_MAP_FARM,
                'check': ISLAND_MAP_FARM_CHECK
            },
            'nursery': {
                'click': ISLAND_MAP_NURSERY,
                'check': ISLAND_MAP_NURSERY_CHECK
            }
        }
        destination_button = button_map.get(destination, {}).get('click')
        check_button = button_map.get(destination, {}).get('check')
        self.goto_island_map()
        while True:
            self.device.screenshot()
            if self.appear(check_button):
                self.device.click(ISLAND_MAP_CONFIRM)
                break
            if self.appear_then_click(destination_button, interval=1):
                pass
        self.goto_management()
        self.ui_goto(page_island)
    def post_manage_mode(self, post_manage_mode):
        post_manage_button = POST_MANAGE_BUSINESS if post_manage_mode == POST_MANAGE_PRODUCTION else POST_MANAGE_PRODUCTION
        while True:
            self.device.screenshot()
            if self.appear_then_click(post_manage_button):
                continue
            elif self.appear(post_manage_mode):
                break

    def select_worker_juu(self):
        while True:
            self.device.screenshot()
            if self.appear(SELECT_WORKER_JUU_Y):
                break
            if self.appear_then_click(SELECT_WORKER_JUU):
                if self.wait_until_appear(SELECT_WORKER_JUU_Y):
                    break
        self.device.click(SELECT_CONFIRM)

    def select_product(self,product_selection,product_selection_check):
        while True:
            self.device.screenshot()
            if self.appear(product_selection_check):
                break
            if self.appear_then_click(product_selection,offset=300):
                continue
            self.device.swipe_vector(vector=(0, -300), box=(333, 142, 431, 602), name="SelectionUpSwipe")


    def post_open(self,post):
        template = TEMPLATE_POST_LOCK
        while True:
            image = self.device.screenshot()
            cell_image = crop(image, post.button)
            if template.match_luma(cell_image, similarity=0.85):
                break
            if self.appear(ISLAND_POST_CHECK):
                break
            if self.appear_then_click(post,offset=50):
                if self.wait_until_appear(ISLAND_POST_CHECK):
                    break
    def post_manage_up_swipe(self,distance):
        self.device.swipe_vector(vector=(0, -distance), box=(688, 69, 725, 656), name="PostUpSwipe")
        self.device.click(ISLAND_WORKING)

    def island_up(self,hold_time):
        p1 = (218, 507)
        p2 = (218, 441)
        self.device.island_swipe_hold(p1, p2,hold_time)

    def island_down(self,hold_time):
        p1 = (218, 507)
        p2 = (218, 572)
        self.device.island_swipe_hold(p1, p2,hold_time)

    def island_right(self,hold_time):
        p1 = (218, 507)
        p2 = (282, 507)
        self.device.island_swipe_hold(p1, p2,hold_time)

    def island_left(self,hold_time):
        p1 = (218, 507)
        p2 = (152, 507)
        self.device.island_swipe_hold(p1, p2,hold_time)



