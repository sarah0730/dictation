# -*- coding: utf-8 -*-
# 2A 词表按学校老师提供的官方听写范围重建（2026-09-30）
# 单元用教材官方名称；老师清单中的话题组并入对应单元
import json

DATA = [
    ("Unit 1 A day out", 1, [
        ("a bus stop", "/ə bʌs stɒp/", "公交车站"),
        ("a cake shop", "/ə keɪk ʃɒp/", "蛋糕店"),
        ("a cinema", "/ə ˈsɪnəmə/", "电影院"),
        ("a clinic", "/ə ˈklɪnɪk/", "诊所"),
        ("a fountain", "/ə ˈfaʊntən/", "喷泉"),
        ("a park", "/ə pɑːk/", "公园"),
        ("a supermarket", "/ə ˈsuːpəmɑːkɪt/", "超市"),
        ("a swimming pool", "/ə ˈswɪmɪŋ puːl/", "游泳池"),
        ("near", "/nɪə/", "在……附近"),
        ("in front of", "/ɪn frʌnt əv/", "在……前面"),
        ("behind", "/bɪˈhaɪnd/", "在……后面"),
        ("between", "/bɪˈtwiːn/", "在……中间"),
        ("mountain", "/ˈmaʊntən/", "山"),
        ("picnic", "/ˈpɪknɪk/", "野餐"),
        ("robot", "/ˈrəʊbɒt/", "机器人"),
    ]),
    ("Unit 2 Let's go!", 2, [
        ("bicycle", "/ˈbaɪsɪkl/", "自行车"),
        ("by bicycle", "/baɪ ˈbaɪsɪkl/", "骑自行车"),
        ("by bus", "/baɪ bʌs/", "乘公交车"),
        ("by car", "/baɪ kɑː/", "坐小汽车"),
        ("by ferry", "/baɪ ˈferi/", "坐渡轮"),
        ("by minibus", "/baɪ ˈmɪnibʌs/", "坐小巴"),
        ("by taxi", "/baɪ ˈtæksi/", "坐出租车"),
        ("by underground", "/baɪ ˈʌndəɡraʊnd/", "坐地铁"),
        ("on foot", "/ɒn fʊt/", "步行"),
        ("birthday party", "/ˈbɜːθdeɪ ˈpɑːti/", "生日派对"),
        ("island", "/ˈaɪlənd/", "岛屿"),
        ("city", "/ˈsɪti/", "城市"),
    ]),
    ("Unit 3 Our school!", 3, [
        ("art room", "/ɑːt ruːm/", "美术室"),
        ("classroom", "/ˈklɑːsruːm/", "教室"),
        ("computer room", "/kəmˈpjuːtə ruːm/", "电脑室"),
        ("hall", "/hɔːl/", "礼堂"),
        ("library", "/ˈlaɪbrəri/", "图书馆"),
        ("music room", "/ˈmjuːzɪk ruːm/", "音乐室"),
        ("playground", "/ˈpleɪɡraʊnd/", "操场"),
        ("ground floor", "/ɡraʊnd flɔː/", "一楼"),
        ("first floor", "/fɜːst flɔː/", "二楼"),
        ("second floor", "/ˈsekənd flɔː/", "三楼"),
        ("third floor", "/θɜːd flɔː/", "四楼"),
        ("fifth floor", "/fɪfθ flɔː/", "五楼"),
        # 校园活动
        ("draw pictures", "/drɔː ˈpɪktʃəz/", "画画"),
        ("have computer lessons", "/hæv kəmˈpjuːtə ˈlesnz/", "上电脑课"),
        ("have lessons", "/hæv ˈlesnz/", "上课"),
        ("play games", "/pleɪ ɡeɪmz/", "玩游戏"),
        ("read books", "/riːd bʊks/", "看书"),
        ("sing songs", "/sɪŋ sɒŋz/", "唱歌"),
        ("watch shows", "/wɒtʃ ʃəʊz/", "看节目"),
    ]),
    ("Unit 4 Our new flat", 4, [
        ("flat", "/flæt/", "公寓"),
        ("sitting room", "/ˈsɪtɪŋ ruːm/", "客厅"),
        ("bathroom", "/ˈbɑːθruːm/", "浴室"),
        ("dining room", "/ˈdaɪnɪŋ ruːm/", "餐厅"),
        ("kitchen", "/ˈkɪtʃɪn/", "厨房"),
        ("bedroom", "/ˈbedruːm/", "卧室"),
        ("storeroom", "/ˈstɔːruːm/", "储藏室"),
        ("study", "/ˈstʌdi/", "书房"),
        # 家务短语
        ("clean the windows", "/kliːn ðə ˈwɪndəʊz/", "擦窗户"),
        ("dust the shelves", "/dʌst ðə ˈʃelvɪz/", "擦拭架子灰尘"),
        ("fold the clothes", "/fəʊld ðə kləʊðz/", "叠衣服"),
        ("make the bed", "/meɪk ðə bed/", "整理床铺"),
        ("set the table", "/set ðə ˈteɪbl/", "摆放餐具"),
        ("sweep the floor", "/swiːp ðə flɔː/", "扫地"),
        ("wash the dishes", "/wɒʃ ðə ˈdɪʃɪz/", "洗碗"),
        ("water the plants", "/ˈwɔːtə ðə plɑːnts/", "给植物浇水"),
        ("shelf", "/ʃelf/", "架子（单数）"),
        ("shelves", "/ʃelvz/", "架子（复数）"),
    ]),
    ("Unit 5 School picnic", 5, [
        ("gloves", "/ɡlʌvz/", "手套"),
        ("a key ring", "/ə kiː rɪŋ/", "钥匙圈"),
        ("a raincoat", "/ə ˈreɪnkəʊt/", "雨衣"),
        ("a scarf", "/ə skɑːf/", "围巾"),
        ("sunglasses", "/ˈsʌnɡlɑːsɪz/", "太阳眼镜"),
        ("an umbrella", "/æn ʌmˈbrelə/", "雨伞"),
        ("a watch", "/ə wɒtʃ/", "手表"),
        ("a water bottle", "/ə ˈwɔːtə ˈbɒtl/", "水瓶"),
        ("picnic", "/ˈpɪknɪk/", "野餐"),
        ("beach", "/biːtʃ/", "沙滩"),
        ("sandwich", "/ˈsænwɪtʃ/", "三明治"),
    ]),
    ("Unit 6 The Honest Woodcutter", 6, [
        ("angry", "/ˈæŋɡri/", "生气的"),
        ("friendly", "/ˈfrendli/", "友好的"),
        ("greedy", "/ˈɡriːdi/", "贪婪的"),
        ("honest", "/ˈɒnɪst/", "诚实的"),
        ("hard-working", "/ˌhɑːd ˈwɜːkɪŋ/", "勤奋的"),
        ("lazy", "/ˈleɪzi/", "懒惰的"),
        ("polite", "/pəˈlaɪt/", "有礼貌的"),
        ("rude", "/ruːd/", "粗鲁无礼的"),
        # 金斧头重点名词
        ("woodcutter", "/ˈwʊdkʌtə/", "樵夫"),
        ("fairy", "/ˈfeəri/", "仙女"),
        ("axe", "/æks/", "斧头"),
        ("gold", "/ɡəʊld/", "黄金"),
        ("silver", "/ˈsɪlvə/", "银"),
        ("wooden", "/ˈwʊdn/", "木头的"),
    ]),
]

# U7 老师补充的扩展单词（按话题分组）
EXT = [
    ("疑问词", [
        ("when", "/wen/", "什么时候"),
        ("how", "/haʊ/", "怎样；如何"),
        ("what", "/wɒt/", "什么"),
        ("why", "/waɪ/", "为什么"),
        ("because", "/bɪˈkɒz/", "因为"),
    ]),
    ("方位&基础词", [
        ("behind", "/bɪˈhaɪnd/", "在……后面"),
        ("now", "/naʊ/", "现在"),
        ("new", "/njuː/", "新的"),
    ]),
    ("指示代词", [
        ("this", "/ðɪs/", "这个"),
        ("these", "/ðiːz/", "这些"),
        ("that", "/ðæt/", "那个"),
        ("those", "/ðəʊz/", "那些"),
    ]),
    ("动作&交流类", [
        ("speaking", "/ˈspiːkɪŋ/", "说（speak 现在分词）"),
        ("chatting", "/ˈtʃætɪŋ/", "聊天（chat 现在分词）"),
        ("communicate", "/kəˈmjuːnɪkeɪt/", "交流，沟通"),
        ("communicating", "/kəˈmjuːnɪkeɪtɪŋ/", "交流（现在分词）"),
        ("talk", "/tɔːk/", "谈话，交谈"),
        ("pointing", "/ˈpɔɪntɪŋ/", "指（point 现在分词）"),
        ("shake", "/ʃeɪk/", "摇晃；握手"),
        ("shake hands", "/ʃeɪk hændz/", "握手"),
        ("say", "/seɪ/", "说"),
        ("said", "/sed/", "说（say 过去式）"),
        ("shouting", "/ˈʃaʊtɪŋ/", "大喊大叫（shout 现在分词）"),
        ("scolding", "/ˈskəʊldɪŋ/", "责骂（scold 现在分词）"),
    ]),
    ("行为动词", [
        ("fight", "/faɪt/", "打架，争斗"),
        ("fighting", "/ˈfaɪtɪŋ/", "打架（现在分词）"),
        ("waste", "/weɪst/", "浪费"),
    ]),
    ("形容词（性格、感受）", [
        ("annoying", "/əˈnɔɪɪŋ/", "令人讨厌的"),
        ("interesting", "/ˈɪntrəstɪŋ/", "有趣的"),
        ("interested", "/ˈɪntrəstɪd/", "感兴趣的"),
        ("boring", "/ˈbɔːrɪŋ/", "无聊的（形容事物）"),
        ("bored", "/bɔːd/", "感到无聊的（形容人）"),
        ("shocked", "/ʃɒkt/", "震惊的"),
        ("polite", "/pəˈlaɪt/", "有礼貌的"),
        ("impolite", "/ˌɪmpəˈlaɪt/", "无礼的"),
        ("honest", "/ˈɒnɪst/", "诚实的"),
        ("friendly", "/ˈfrendli/", "友好的"),
        ("helpful", "/ˈhelpfl/", "乐于助人的"),
        ("kind", "/kaɪnd/", "善良的"),
        ("naughty", "/ˈnɔːti/", "淘气的"),
        ("lazy", "/ˈleɪzi/", "懒惰的"),
        ("hard-working", "/ˌhɑːd ˈwɜːkɪŋ/", "勤奋的"),
    ]),
    ("名词", [
        ("school", "/skuːl/", "学校"),
        ("activity", "/ækˈtɪvəti/", "活动"),
        ("backpack", "/ˈbækpæk/", "背包"),
        ("milk", "/mɪlk/", "牛奶"),
        ("person", "/ˈpɜːsn/", "人"),
    ]),
    ("常用句型", [
        ("It is time to…", "", "是……的时候了"),
        ("Yes, they are.", "", "是的，他们是。"),
        ("No, it is not.", "", "不，它不是。"),
        ("No, they are not.", "", "不，他们不是。"),
        ("It is…", "", "它是……"),
        ("It is polite.", "", "这是有礼貌的。"),
    ]),
]

new_words = []
seq = 0
for unit, unitNum, words in DATA:
    for w, ph, m in words:
        seq += 1
        new_words.append({
            "seq": seq, "book": "2A", "unit": unit, "unitNum": unitNum,
            "word": w, "phonetic": ph, "meaning": m, "pos": "", "level": "",
        })
for topic, words in EXT:
    for w, ph, m in words:
        seq += 1
        new_words.append({
            "seq": seq, "book": "2A", "unit": "Unit 7 扩展单词", "unitNum": 7,
            "word": w, "phonetic": ph, "meaning": m, "pos": "", "level": "",
            "topic": topic,
        })

# U8 自然拼读单词（按拼读规则分组）
PHONICS = [
    ("Unit1 ai（发音 /eɪ/）", [
        ("rain", "/reɪn/", "雨；下雨"),
        ("wait", "/weɪt/", "等待"),
        ("train", "/treɪn/", "火车"),
        ("tail", "/teɪl/", "尾巴"),
        ("snail", "/sneɪl/", "蜗牛"),
        ("Spain", "/speɪn/", "西班牙"),
    ]),
    ("Unit1 ay（发音 /eɪ/）", [
        ("day", "/deɪ/", "日子，天"),
        ("May", "/meɪ/", "五月"),
        ("way", "/weɪ/", "道路，方法"),
        ("play", "/pleɪ/", "玩耍"),
        ("clay", "/kleɪ/", "黏土"),
        ("today", "/təˈdeɪ/", "今天"),
    ]),
    ("Unit2 oi（发音 /ɔɪ/）", [
        ("oil", "/ɔɪl/", "油"),
        ("boil", "/bɔɪl/", "煮沸"),
        ("coin", "/kɔɪn/", "硬币"),
        ("soil", "/sɔɪl/", "泥土"),
        ("joint", "/dʒɔɪnt/", "关节，连接处"),
    ]),
    ("Unit2 oy（发音 /ɔɪ/）", [
        ("boy", "/bɔɪ/", "男孩"),
        ("toy", "/tɔɪ/", "玩具"),
        ("joy", "/dʒɔɪ/", "快乐"),
        ("Roy", "/rɔɪ/", "罗伊（人名）"),
    ]),
    ("Unit3 oa（发音 /əʊ/）", [
        ("oat", "/əʊt/", "燕麦"),
        ("goat", "/ɡəʊt/", "山羊"),
        ("oak", "/əʊk/", "橡树"),
        ("road", "/rəʊd/", "马路"),
        ("toad", "/təʊd/", "蟾蜍，癞蛤蟆"),
        ("coach", "/kəʊtʃ/", "长途大巴；教练"),
        ("toast", "/təʊst/", "烤面包片"),
        ("boat", "/bəʊt/", "小船"),
    ]),
]
for topic, words in PHONICS:
    for w, ph, m in words:
        seq += 1
        new_words.append({
            "seq": seq, "book": "2A", "unit": "Unit 8 自然拼读", "unitNum": 8,
            "word": w, "phonetic": ph, "meaning": m, "pos": "", "level": "",
            "topic": topic,
        })

with open('words.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

old = {w['word'].strip().lower() for w in d['2A']}
new = {w['word'].strip().lower() for w in new_words}

d['2A'] = new_words
with open('words.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=1)

print('2A 重建完成：', len(new_words), '词,', len(DATA), '组')
print('\n== 老师清单里有、旧表没有（新增）==')
for x in sorted(new - old): print(' +', x)
print('\n== 旧表里有、老师清单没有（移除）== 共', len(old - new), '词')
for x in sorted(old - new): print(' -', x)
