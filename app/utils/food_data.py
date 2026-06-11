"""
内置食物数据库：约 100 种青少年高频食物
每条包含：name, category, sub_category, light_color
"""

FOOD_DATABASE = [
    # ======= 蔬菜类 (绿灯) =======
    {"name": "番茄炒蛋", "category": "蔬菜", "sub_category": "炒菜", "light_color": "green"},
    {"name": "炒青菜", "category": "蔬菜", "sub_category": "绿叶蔬菜", "light_color": "green"},
    {"name": "蒜蓉西兰花", "category": "蔬菜", "sub_category": "绿叶蔬菜", "light_color": "green"},
    {"name": "清炒菠菜", "category": "蔬菜", "sub_category": "绿叶蔬菜", "light_color": "green"},
    {"name": "凉拌黄瓜", "category": "蔬菜", "sub_category": "凉拌菜", "light_color": "green"},
    {"name": "炒白菜", "category": "蔬菜", "sub_category": "绿叶蔬菜", "light_color": "green"},
    {"name": "炒生菜", "category": "蔬菜", "sub_category": "绿叶蔬菜", "light_color": "green"},
    {"name": "炒空心菜", "category": "蔬菜", "sub_category": "绿叶蔬菜", "light_color": "green"},
    {"name": "凉拌西红柿", "category": "蔬菜", "sub_category": "凉拌菜", "light_color": "green"},
    {"name": "拍黄瓜", "category": "蔬菜", "sub_category": "凉拌菜", "light_color": "green"},
    {"name": "炒豆芽", "category": "蔬菜", "sub_category": "豆类", "light_color": "green"},
    {"name": "蒸南瓜", "category": "蔬菜", "sub_category": "根茎类", "light_color": "green"},
    {"name": "煮玉米", "category": "蔬菜", "sub_category": "杂粮", "light_color": "green"},
    {"name": "炒茄子", "category": "蔬菜", "sub_category": "炒菜", "light_color": "green"},
    {"name": "炒芹菜", "category": "蔬菜", "sub_category": "绿叶蔬菜", "light_color": "green"},

    # ======= 水果类 (绿灯) =======
    {"name": "苹果", "category": "水果", "sub_category": "鲜果", "light_color": "green"},
    {"name": "香蕉", "category": "水果", "sub_category": "鲜果", "light_color": "green"},
    {"name": "橙子", "category": "水果", "sub_category": "鲜果", "light_color": "green"},
    {"name": "葡萄", "category": "水果", "sub_category": "鲜果", "light_color": "green"},
    {"name": "西瓜", "category": "水果", "sub_category": "鲜果", "light_color": "green"},
    {"name": "草莓", "category": "水果", "sub_category": "鲜果", "light_color": "green"},
    {"name": "蓝莓", "category": "水果", "sub_category": "鲜果", "light_color": "green"},
    {"name": "梨", "category": "水果", "sub_category": "鲜果", "light_color": "green"},
    {"name": "桃子", "category": "水果", "sub_category": "鲜果", "light_color": "green"},
    {"name": "猕猴桃", "category": "水果", "sub_category": "鲜果", "light_color": "green"},

    # ======= 优质蛋白 (绿灯) =======
    {"name": "鸡胸肉", "category": "优质蛋白", "sub_category": "白肉", "light_color": "green"},
    {"name": "鸡蛋", "category": "优质蛋白", "sub_category": "蛋类", "light_color": "green"},
    {"name": "清蒸鱼", "category": "优质蛋白", "sub_category": "海鲜", "light_color": "green"},
    {"name": "虾仁", "category": "优质蛋白", "sub_category": "海鲜", "light_color": "green"},
    {"name": "豆腐", "category": "优质蛋白", "sub_category": "豆制品", "light_color": "green"},
    {"name": "豆浆", "category": "优质蛋白", "sub_category": "豆制品", "light_color": "green"},
    {"name": "瘦牛肉", "category": "优质蛋白", "sub_category": "红肉", "light_color": "green"},
    {"name": "三文鱼", "category": "优质蛋白", "sub_category": "海鲜", "light_color": "green"},
    {"name": "纯牛奶", "category": "优质蛋白", "sub_category": "乳制品", "light_color": "green"},
    {"name": "酸奶", "category": "优质蛋白", "sub_category": "乳制品", "light_color": "green"},

    # ======= 全谷物 (绿灯) =======
    {"name": "燕麦粥", "category": "全谷物", "sub_category": "杂粮", "light_color": "green"},
    {"name": "糙米饭", "category": "全谷物", "sub_category": "杂粮", "light_color": "green"},
    {"name": "全麦面包", "category": "全谷物", "sub_category": "面包", "light_color": "green"},
    {"name": "红薯", "category": "全谷物", "sub_category": "杂粮", "light_color": "green"},
    {"name": "紫薯", "category": "全谷物", "sub_category": "杂粮", "light_color": "green"},

    # ======= 精制主食 (黄灯) =======
    {"name": "白米饭", "category": "精制主食", "sub_category": "主食", "light_color": "yellow"},
    {"name": "馒头", "category": "精制主食", "sub_category": "主食", "light_color": "yellow"},
    {"name": "面条", "category": "精制主食", "sub_category": "主食", "light_color": "yellow"},
    {"name": "白面包", "category": "精制主食", "sub_category": "面包", "light_color": "yellow"},
    {"name": "花卷", "category": "精制主食", "sub_category": "主食", "light_color": "yellow"},
    {"name": "包子", "category": "精制主食", "sub_category": "主食", "light_color": "yellow"},
    {"name": "饺子", "category": "精制主食", "sub_category": "主食", "light_color": "yellow"},
    {"name": "馄饨", "category": "精制主食", "sub_category": "主食", "light_color": "yellow"},

    # ======= 瘦肉/豆制品 (黄灯) =======
    {"name": "猪肉丝", "category": "瘦肉", "sub_category": "红肉", "light_color": "yellow"},
    {"name": "红烧肉", "category": "瘦肉", "sub_category": "红肉", "light_color": "yellow"},
    {"name": "肉包子", "category": "瘦肉", "sub_category": "混合", "light_color": "yellow"},
    {"name": "肉夹馍", "category": "瘦肉", "sub_category": "混合", "light_color": "yellow"},
    {"name": "腐竹", "category": "瘦肉", "sub_category": "豆制品", "light_color": "yellow"},
    {"name": "豆干", "category": "瘦肉", "sub_category": "豆制品", "light_color": "yellow"},

    # ======= 炒菜/混合 (黄灯) =======
    {"name": "宫保鸡丁", "category": "炒菜", "sub_category": "川菜", "light_color": "yellow"},
    {"name": "鱼香肉丝", "category": "炒菜", "sub_category": "川菜", "light_color": "yellow"},
    {"name": "土豆丝", "category": "炒菜", "sub_category": "家常菜", "light_color": "yellow"},
    {"name": "麻婆豆腐", "category": "炒菜", "sub_category": "川菜", "light_color": "yellow"},
    {"name": "回锅肉", "category": "炒菜", "sub_category": "川菜", "light_color": "yellow"},
    {"name": "糖醋排骨", "category": "炒菜", "sub_category": "家常菜", "light_color": "yellow"},
    {"name": "炒面", "category": "炒菜", "sub_category": "主食", "light_color": "yellow"},
    {"name": "炒饭", "category": "炒菜", "sub_category": "主食", "light_color": "yellow"},
    {"name": "盖浇饭", "category": "炒菜", "sub_category": "主食+菜", "light_color": "yellow"},
    {"name": "兰州拉面", "category": "炒菜", "sub_category": "面食", "light_color": "yellow"},
    {"name": "重庆小面", "category": "炒菜", "sub_category": "面食", "light_color": "yellow"},
    {"name": "蛋炒饭", "category": "炒菜", "sub_category": "主食", "light_color": "yellow"},

    # ======= 油炸/高脂 (红灯) =======
    {"name": "炸鸡", "category": "油炸", "sub_category": "炸物", "light_color": "red"},
    {"name": "薯条", "category": "油炸", "sub_category": "炸物", "light_color": "red"},
    {"name": "炸鸡排", "category": "油炸", "sub_category": "炸物", "light_color": "red"},
    {"name": "炸串", "category": "油炸", "sub_category": "炸物", "light_color": "red"},
    {"name": "烤串", "category": "油炸", "sub_category": "烧烤", "light_color": "red"},
    {"name": "汉堡", "category": "油炸", "sub_category": "快餐", "light_color": "red"},
    {"name": "披萨", "category": "油炸", "sub_category": "快餐", "light_color": "red"},
    {"name": "麻辣烫", "category": "油炸", "sub_category": "重口味", "light_color": "red"},
    {"name": "火锅", "category": "油炸", "sub_category": "重口味", "light_color": "red"},
    {"name": "烧烤", "category": "油炸", "sub_category": "烧烤", "light_color": "red"},
    {"name": "煎饼果子", "category": "油炸", "sub_category": "街头小吃", "light_color": "red"},
    {"name": "手抓饼", "category": "油炸", "sub_category": "街头小吃", "light_color": "red"},
    {"name": "辣条", "category": "油炸", "sub_category": "零食", "light_color": "red"},
    {"name": "方便面", "category": "油炸", "sub_category": "速食", "light_color": "red"},
    {"name": "油条", "category": "油炸", "sub_category": "炸物", "light_color": "red"},

    # ======= 甜点/零食 (红灯) =======
    {"name": "蛋糕", "category": "甜点", "sub_category": "甜食", "light_color": "red"},
    {"name": "冰淇淋", "category": "甜点", "sub_category": "甜食", "light_color": "red"},
    {"name": "巧克力", "category": "甜点", "sub_category": "甜食", "light_color": "red"},
    {"name": "饼干", "category": "甜点", "sub_category": "零食", "light_color": "red"},
    {"name": "薯片", "category": "甜点", "sub_category": "零食", "light_color": "red"},
    {"name": "蛋挞", "category": "甜点", "sub_category": "甜食", "light_color": "red"},
    {"name": "甜甜圈", "category": "甜点", "sub_category": "甜食", "light_color": "red"},
    {"name": "奶油泡芙", "category": "甜点", "sub_category": "甜食", "light_color": "red"},
    {"name": "糖果", "category": "甜点", "sub_category": "零食", "light_color": "red"},
    {"name": "锅巴", "category": "甜点", "sub_category": "零食", "light_color": "red"},

    # ======= 含糖饮料 (红灯) =======
    {"name": "奶茶", "category": "含糖饮料", "sub_category": "饮料", "light_color": "red"},
    {"name": "可乐", "category": "含糖饮料", "sub_category": "饮料", "light_color": "red"},
    {"name": "果汁饮料", "category": "含糖饮料", "sub_category": "饮料", "light_color": "red"},
    {"name": "雪碧", "category": "含糖饮料", "sub_category": "饮料", "light_color": "red"},
    {"name": "冰红茶", "category": "含糖饮料", "sub_category": "饮料", "light_color": "red"},
    {"name": "乳酸菌饮料", "category": "含糖饮料", "sub_category": "饮料", "light_color": "red"},
    {"name": "气泡水", "category": "含糖饮料", "sub_category": "饮料", "light_color": "yellow"},
    {"name": "功能饮料", "category": "含糖饮料", "sub_category": "饮料", "light_color": "red"},
    {"name": "拿铁咖啡", "category": "含糖饮料", "sub_category": "咖啡", "light_color": "yellow"},
    {"name": "美式咖啡", "category": "含糖饮料", "sub_category": "咖啡", "light_color": "green"},

    # ======= 补充：食堂/外卖高频菜 =======
    {"name": "黄焖鸡", "category": "炒菜", "sub_category": "食堂菜", "light_color": "yellow"},
    {"name": "红烧排骨", "category": "炒菜", "sub_category": "家常菜", "light_color": "yellow"},
    {"name": "酸辣土豆丝", "category": "炒菜", "sub_category": "家常菜", "light_color": "yellow"},
    {"name": "青椒肉丝", "category": "炒菜", "sub_category": "家常菜", "light_color": "yellow"},
    {"name": "地三鲜", "category": "炒菜", "sub_category": "东北菜", "light_color": "yellow"},
    {"name": "红烧茄子", "category": "炒菜", "sub_category": "家常菜", "light_color": "yellow"},
    {"name": "醋溜白菜", "category": "蔬菜", "sub_category": "绿叶蔬菜", "light_color": "green"},
    {"name": "香菇油菜", "category": "蔬菜", "sub_category": "绿叶蔬菜", "light_color": "green"},
    {"name": "水煮鱼", "category": "炒菜", "sub_category": "川菜", "light_color": "yellow"},
    {"name": "酸菜鱼", "category": "炒菜", "sub_category": "川菜", "light_color": "yellow"},
    {"name": "小炒肉", "category": "炒菜", "sub_category": "湘菜", "light_color": "yellow"},
    {"name": "大盘鸡", "category": "炒菜", "sub_category": "西北菜", "light_color": "yellow"},
    {"name": "螺蛳粉", "category": "油炸", "sub_category": "重口味", "light_color": "red"},
    {"name": "麻辣香锅", "category": "油炸", "sub_category": "重口味", "light_color": "red"},
    {"name": "冒菜", "category": "油炸", "sub_category": "重口味", "light_color": "red"},
]


def search_foods(query: str, limit: int = 20) -> list[dict]:
    """模糊搜索食物"""
    query_lower = query.strip().lower()
    results = []
    for food in FOOD_DATABASE:
        if query_lower in food["name"].lower():
            results.append(food)
        if len(results) >= limit:
            break
    return results


def classify_light_color(category: str) -> str:
    """根据类别返回红黄绿灯颜色"""
    green_categories = {"蔬菜", "水果", "优质蛋白", "全谷物"}
    yellow_categories = {"精制主食", "瘦肉", "豆制品", "炒菜"}
    red_categories = {"油炸", "甜点", "含糖饮料"}

    if category in green_categories:
        return "green"
    elif category in yellow_categories:
        return "yellow"
    elif category in red_categories:
        return "red"
    return "yellow"
