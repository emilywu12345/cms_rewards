"""
Gift测试数据
"""

# Gift测试数据
GIFT_TEST_DATA = {
    "auto_gift_1": {
        "gift_create_url":"https://admincms-uat-cicd.splusrewards.com.hk/gift/create",
        "thumbnail_file": "C:\\Users\\User\\File\\S+\\testImage\\Gift\\thumbnailImage.png",
        "content_file": "C:\\Users\\User\\File\\S+\\testImage\\Gift\\contentImage.png",
        "remarks": "Auto Test Gift",
        "points": "100",
        "value": "20",
        "cost": "10",
        "gift_name_en": "Auto Test Gift",
        "gift_name_zh": "自动测试礼物",
        "gift_name_zh_hk": "自動測試禮物",
        "sku_number": "10",
        "stock": "12"
    }
}

# def get_gift_data(data_key):
#     """获取礼物测试数据
    
#     Args:
#         data_key: 数据键值，如 "auto_gift_1" 或 "test_gift_hotel"
    
#     Returns:
#         dict: 礼物测试数据
#     """
#     # 如果请求的是 test_gift_hotel，返回 auto_gift_1 的数据
#     if data_key == "test_gift_hotel":
#         return GIFT_TEST_DATA["auto_gift_1"]
    
#     # 否则直接根据键值返回
#     return GIFT_TEST_DATA.get(data_key, GIFT_TEST_DATA["auto_gift_1"])