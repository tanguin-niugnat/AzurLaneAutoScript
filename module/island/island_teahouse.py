from module.island_teahouse.assets import *
from module.island.island_shop_base import IslandShopBase
from module.island.assets import *
from module.ui.page import *


class IslandTeahouse(IslandShopBase):
    def __init__(self, config, device=None, task=None):
        super().__init__(config=config, device=device, task=task)

        # 设置店铺类型
        self.shop_type = "teahouse"
        self.time_prefix = "time_tea"
        self.chef_config = self.config.IslandTeahouse_Chef

        # 设置商品列表
        self.shop_items = [
            {'name': 'apple_juice', 'template': TEMPLATE_APPLE_JUICE, 'var_name': 'apple_juice',
             'selection': SELECT_APPLE_JUICE, 'selection_check': SELECT_APPLE_JUICE_CHECK,
             'post_action': POST_APPLE_JUICE},
            {'name': 'banana_mango', 'template': TEMPLATE_BANANA_MANGO, 'var_name': 'banana_mango',
             'selection': SELECT_BANANA_MANGO, 'selection_check': SELECT_BANANA_MANGO_CHECK,
             'post_action': POST_BANANA_MANGO},
            {'name': 'honey_lemon', 'template': TEMPLATE_HONEY_LEMON, 'var_name': 'honey_lemon',
             'selection': SELECT_HONEY_LEMON, 'selection_check': SELECT_HONEY_LEMON_CHECK,
             'post_action': POST_HONEY_LEMON},
            {'name': 'strawberry_lemon', 'template': TEMPLATE_STRAWBERRY_LEMON, 'var_name': 'strawberry_lemon',
             'selection': SELECT_STRAWBERRY_LEMON, 'selection_check': SELECT_STRAWBERRY_LEMON_CHECK,
             'post_action': POST_STRAWBERRY_LEMON},
            {'name': 'strawberry_honey', 'template': TEMPLATE_STRAWBERRY_HONEY, 'var_name': 'strawberry_honey',
             'selection': SELECT_STRAWBERRY_HONEY, 'selection_check': SELECT_STRAWBERRY_HONEY_CHECK,
             'post_action': POST_STRAWBERRY_HONEY},
            {'name': 'floral_fruity', 'template': TEMPLATE_FLORAL_FRUITY, 'var_name': 'floral_fruity',
             'selection': SELECT_FLORAL_FRUITY, 'selection_check': SELECT_FLORAL_FRUITY_CHECK,
             'post_action': POST_FLORAL_FRUITY},
            {'name': 'fruit_paradise', 'template': TEMPLATE_FRUIT_PARADISE, 'var_name': 'fruit_paradise',
             'selection': SELECT_FRUIT_PARADISE, 'selection_check': SELECT_FRUIT_PARADISE_CHECK,
             'post_action': POST_FRUIT_PARADISE},
            {'name': 'lavender_tea', 'template': TEMPLATE_LAVENDER_TEA, 'var_name': 'lavender_tea',
             'selection': SELECT_LAVENDER_TEA, 'selection_check': SELECT_LAVENDER_TEA_CHECK,
             'post_action': POST_LAVENDER_TEA},
            {'name': 'sunny_honey', 'template': TEMPLATE_SUNNY_HONEY, 'var_name': 'sunny_honey',
             'selection': SELECT_SUNNY_HONEY, 'selection_check': SELECT_SUNNY_HONEY_CHECK,
             'post_action': POST_SUNNY_HONEY},
        ]

        # 设置套餐组成
        self.meal_compositions = {
            'floral_fruity': {
                'required': ['lavender_tea', 'apple_juice'],
                'quantity_per': 1
            },
            'fruit_paradise': {
                'required': ['banana_mango', 'strawberry_honey'],
                'quantity_per': 1
            },
            'sunny_honey': {
                'required': ['strawberry_lemon', 'honey_lemon'],
                'quantity_per': 1
            }
        }

        # 设置岗位按钮
        self.post_buttons = {
            'ISLAND_TEAHOUSE_POST1': ISLAND_TEAHOUSE_POST1,
            'ISLAND_TEAHOUSE_POST2': ISLAND_TEAHOUSE_POST2
        }

        # 设置筛选资产
        self.filter_asset = FILTER_ISLAND_TEAHOUSE

        # 设置配置前缀
        self.setup_config(
            config_meal_prefix="IslandTeahouse_Meal",
            config_number_prefix="IslandTeahouse_MealNumber",
            config_task_prefix="IslandTeahouseNextTask_MealTask",
            config_task_number_prefix="IslandTeahouseNextTask_MealTaskNumber",
            config_post_number="IslandTeahouse_PostNumber",
            config_away_cook="IslandTeahouseNextTask_AwayCook"
        )

        # 特殊材料：蜂蜜
        self.fresh_honey = 0
        self.initialize_shop()

    def get_warehouse_counts(self):
        """覆盖：获取仓库数量，包括蜂蜜"""
        # 先调用父类方法获取基础库存
        super().get_warehouse_counts()

        # 额外获取蜂蜜数量
        self.ui_goto(page_island_warehouse_filter)
        self.appear_then_click(FILTER_RESET)
        self.appear_then_click(FILTER_BASIC)
        self.appear_then_click(FILTER_OTHER)
        self.appear_then_click(FILTER_CONFIRM)
        self.device.sleep(0.3)
        image = self.device.screenshot()
        self.fresh_honey = self.ocr_item_quantity(image, TEMPLATE_FRESH_HONEY)
        print(f"蜂蜜数量: {self.fresh_honey}")

        # 将蜂蜜库存存入warehouse_counts，便于统一处理
        self.warehouse_counts['fresh_honey'] = self.fresh_honey

        # ============ 新增：检查蜂蜜任务并添加到高优先级 ============
        if (self.config.IslandTeahouse_SunnyHoney and
                self.fresh_honey > 0):

            # 计算可以生产的sunny_honey数量
            strawberry_lemon_stock = self.warehouse_counts.get('strawberry_lemon', 0)
            honey_lemon_stock = self.warehouse_counts.get('honey_lemon', 0)

            # sunny_honey需要strawberry_lemon和honey_lemon各1个
            max_by_strawberry = strawberry_lemon_stock
            max_by_honey_lemon = honey_lemon_stock
            max_sunny_honey = min(max_by_strawberry, max_by_honey_lemon)

            if max_sunny_honey > 0:
                # 添加到高优先级任务
                self.add_high_priority_product('sunny_honey', max_sunny_honey)
                print(f"检测到蜂蜜任务，高优先级生产: sunny_honey x{max_sunny_honey}")
        # ========================================================

        return self.warehouse_counts

    def check_material_limits(self, product, batch_size):
        """覆盖：检查材料限制，包括蜂蜜和蜂蜜柠檬原材料"""
        # 先调用父类方法检查套餐原材料
        batch_size = super().check_material_limits(product, batch_size)

        if batch_size <= 0:
            return 0

        # 蜂蜜柠檬需要检查蜂蜜
        if product == 'honey_lemon':
            possible_batch = min(batch_size, self.fresh_honey)
            if possible_batch <= 0:
                print(f"生产 {product} 的蜂蜜不足")
                return 0
            batch_size = possible_batch

        # sunny_honey套餐中的honey_lemon需要蜂蜜
        if product == 'sunny_honey':
            # sunny_honey需要honey_lemon和strawberry_lemon
            # 已经通过父类检查了这两种原材料
            # 还需要检查honey_lemon是否有足够的蜂蜜
            honey_lemon_needed = batch_size
            honey_needed = honey_lemon_needed  # 1个honey_lemon需要1个蜂蜜
            possible_by_honey = min(batch_size, self.fresh_honey // 1)
            batch_size = possible_by_honey

        return batch_size

    def deduct_materials(self, product, number):
        """覆盖：扣除前置材料，包括蜂蜜和套餐原材料"""
        # 先调用父类方法扣除套餐原材料
        super().deduct_materials(product, number)

        # 蜂蜜柠檬需要扣除蜂蜜
        if product == 'honey_lemon':
            honey_needed = number
            self.fresh_honey -= honey_needed
            if 'fresh_honey' in self.warehouse_counts:
                self.warehouse_counts['fresh_honey'] -= honey_needed
            print(f"扣除蜂蜜：fresh_honey -{honey_needed}")

        # sunny_honey套餐中的honey_lemon也需要扣除蜂蜜
        if product == 'sunny_honey':
            # sunny_honey需要honey_lemon，每个需要1个蜂蜜
            honey_needed = number
            self.fresh_honey -= honey_needed
            if 'fresh_honey' in self.warehouse_counts:
                self.warehouse_counts['fresh_honey'] -= honey_needed
            print(f"扣除蜂蜜（用于sunny_honey）：fresh_honey -{honey_needed}")

    def apply_special_material_constraints(self, requirements):
        """覆盖：根据蜂蜜库存调整需求"""
        result = requirements.copy()

        # 处理蜂蜜限制
        # 检查所有需要蜂蜜的产品
        for product in ['honey_lemon', 'sunny_honey']:
            if product in result and result[product] > 0:
                if product == 'honey_lemon':
                    honey_needed = result[product]
                elif product == 'sunny_honey':
                    honey_needed = result[product]  # 每个sunny_honey需要1个蜂蜜（通过honey_lemon）

                if self.fresh_honey < honey_needed:
                    # 调整需求
                    max_by_honey = self.fresh_honey
                    result[product] = max_by_honey
                    print(f"蜂蜜不足，将{product}需求从{honey_needed}调整为{max_by_honey}")

        return result


if __name__ == "__main__":
    az = IslandTeahouse('alas', task='Alas')
    az.device.screenshot()
    az.run()