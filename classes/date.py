import re
from datetime import datetime
from dateutil.parser import parser, parserinfo


## 全角文字列は半角に統一しましょう
ZEN = '！＂＃＄％＆＇（）＊＋，－．／０１２３４５６７８９：；＜＝＞？＠ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ［＼］＾＿｀ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ｛｜｝～'
HAN = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
def to_hankaku(s):
    return s.translate(str.maketrans(ZEN, HAN))

## 漢数字は使わずアラビア数字にしましょう
def kanji2int(s,
    kns = str.maketrans('一二三四五六七八九〇壱弐参', '1234567890123'),
    re_kn = re.compile(r'[十拾百千万億兆\d]+'),
    re_ku1 = re.compile(r'[十拾百千]|\d+'),
    re_ku2 = re.compile(r'[万億兆]|[^万億兆]+'),
    UNIT1 = {'十': 10,
            '拾': 10,
            '百': 100,
            '千': 1000},
    UNIT2 = {'万': 10000,
            '億': 100000000,
            '兆': 1000000000000}
    ):
    def _tran(sj, re_obj=re_ku1, transdic=UNIT1):
        unit = 1
        result = 0
        for piece in reversed(re_obj.findall(sj)):
            if piece in transdic:
                if unit > 1:
                    result += unit
                unit = transdic[piece]
            else:
                val = int(piece) if piece.isdecimal() else _tran(piece)
                result += val * unit
                unit = 1

        if unit > 1:
            result += unit

        return result

    ret = s.translate(kns)
    for num in sorted(set(re_kn.findall(ret)), key=lambda s: len(s), reverse=True):
        if not num.isdecimal():
            ar = _tran(num, re_ku2, UNIT2)
            ret = ret.replace(num, str(ar))

    return ret


## 午前午後の位置がおかしい場合もあるので、AM,PMの位置を補正する関数
_ng_ampm = re.compile('(\\s*(?:[AaPp]\\.?[Mm]\\.?|午[前後]))((?:\\s*(?:1[0-9]|2[0-4]||0?[0-9])\\s*?[\\.:時]?\\s*(?:[1-5][0-9]|0?[0-9])\\s*?[\\.:分]?\\s*(?:[1-5][0-9]|0?[0-9])\\s*?(?:秒|[Ss]ec(?:onds)?)??\\s*(?:[,\\.]?\\d+)?(?:\\s*(?:[+\\-]\\d{4})\\s*\\(?(?:[ABCDEFGHIJKLMNOPRSTUVWY][ABCDEFGHIJKLMNOPRSTUVWXYZ][ABCDGHKLMNORSTUVWZ][1DST][T])\\)?|\\s*(?:[+\\-]\\d{4})|\\s*\\(?(?:[ABCDEFGHIJKLMNOPRSTUVWY][ABCDEFGHIJKLMNOPRSTUVWXYZ][ABCDGHKLMNORSTUVWZ][1DST][T])\\)?)?)[^\\s]*)')
def repair_ampm(s):
    return _ng_ampm.sub(" \\2 \\1", s).replace("  ", " ")


## 元号を使った和暦表現はやめて西暦にしましょう
g2d = {
    '令和': datetime(2019, 5, 1),
    'R': datetime(2019, 5, 1),
    '平成': datetime(1989, 1, 8),
    'H': datetime(1989, 1, 8),
    '昭和': datetime(1926, 12, 25),
    'S': datetime(1926, 12, 25),
    '大正': datetime(1912, 7, 30),
    'T': datetime(1912, 7, 30),
    '明治': datetime(1868, 10, 23),
    'M': datetime(1868, 10, 23),
}

## 和暦で1年の時だけ、元年という表現が許されているのは困ります
def gengo2date(timestr):
    g = next((d for d in g2d if d in timestr), None)
    if g is None:
        return timestr

    dy = g2d[g]
    i = dy.year - 1
    pattern = r"(?:" + g + r"[\.,\- ]?)((?:[0-9]{1,2}|元))\s?(年?)"

    reret = re.search(pattern, timestr)
    if reret:
        n = reret.group(1)
        edit = "{}{}".format(int("1" if n == "元" else n) + i, reret.group(2))
        return timestr.replace(reret.group(0), edit)

    return timestr

## dateutilのクラスを一部継承して拡張します
class lazydate(object):
    class jpinfo(parserinfo):
        JUMP = [" ", "　",".", ",", ";", "-", "/", "'",
                "at", "on", "and", "ad", "m", "t", "of",
                "st", "nd", "rd", "th",
                "年", "月", "日",
                ]
        HMS = [("h", "hour", "hours", "時"),
               ("m", "minute", "minutes", "分"),
               ("s", "second", "seconds", "秒")]
        AMPM = [("am", "a", "午前"),
                ("pm", "p", "午後")]

    def __init__(self, timestr, parserinfo=None, **kwargs):
        self._dt = None
        self.timestr = timestr
        self.parserinfo = parserinfo or __class__.jpinfo()
        self._kwargs = kwargs

        if isinstance(timestr, datetime):
            self._dt = timestr
            self.timestr = self.repairstr = str(timestr)

        if not isinstance(timestr, str):
            self.timestr = str(timestr)

        if "fuzzy" not in kwargs:
            self._kwargs["fuzzy"] = True

    def parse(self, timestr=None, **kw):
        if timestr is None and self._dt is not None:
            return self._dt
        if isinstance(timestr, datetime):
            return timestr

        repairstr = to_hankaku(timestr or self.timestr)
        repairstr = kanji2int(repairstr)
        repairstr = gengo2date(repairstr)
        repairstr = repair_ampm(repairstr)

        return parser(self.parserinfo).parse(repairstr, **{**self._kwargs, **kw})


## 細かい表現方法の違いは気にせずとにかく、datetimeオブジェクトが欲しいだけなのです
def to_datetime(timestr):
    return lazydate(timestr).parse(fuzzy_with_tokens=False).date()


if __name__=="__main__":
    a = "2023年5月23日"
    print(to_datetime(a).date())