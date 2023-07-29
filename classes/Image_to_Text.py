# インストールしたもの
# pip install openai
# pip install requests
import json
import requests
import time 
import codecs
import openai
import os

def image_to_text(FoldaPath):
    # ocr部分
    # 画像ファイルを分析可能な形にしてjsonファイルに作り替える
    subscription_key = "dbbdab1491fe4cf285d3e2ed1f334927" ##### 中村ゼミのocrAPIなので悪用厳禁! (ゼミのクレカから使用する分だけ料金が落とされるので、極力使わないこと!)
    endpoint = "https://rnmuds.cognitiveservices.azure.com/" ##### 中村ゼミのocrAPIなので悪用厳禁!(ゼミのクレカから使用する分だけ料金が落とされるので、極力使わないこと!)
    text_recognition_url = endpoint + "vision/v3.2/read/analyze"
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-Type':'application/octet-stream'  }
    params   = { 'language ': 'ja',
                'model-version':'2021-04-12'}
    
    image_list = os.listdir(FoldaPath)

    count = 0
    lines = []
    output = ""

    for File in image_list:
        image_file = FoldaPath + "/" + File
        with open(image_file, 'rb') as f:
            data = f.read()

        # 指定した画像の read メソッドを呼び出します。これによって operation ID が返され、画像の内容を読み取る非同期プロセスが開始されます
        response = requests.post(text_recognition_url, headers=headers, params=params, json=None, data=data)
        response.raise_for_status()

        # レスポンスから operation location（末尾にIDが付いたURL）を取得する
        operation_url = response.headers["Operation-Location"]
        analysis = {}
        poll = True

        # read の呼び出しから返された operation location ID を取得し、操作の結果をサービスに照会します。 
        # 次のコードは、結果が返されるまで 1 秒間隔で操作をチェックします
        while (poll):
            response_final = requests.get(response.headers["Operation-Location"], headers=headers)
            analysis = response_final.json()

            # print(json.dumps(analysis, indent=4, ensure_ascii=False))

            time.sleep(1)
            if ("analyzeResult" in analysis):
                poll = False
            if ("status" in analysis and analysis['status'] == 'failed'):
                poll = False

        # JSON ファイルを出力
        with codecs.open('output_read3.2.json', 'w+', 'utf-8') as fp:
            json.dump(analysis, fp, ensure_ascii=False, indent=2)

        ## 画像ファイルから文字起こし
        with open('./output_read3.2.json', 'r', encoding='utf-8') as f:
            analysis = json.load(f)

        if ("analyzeResult" in analysis):
            lines = [(line["boundingBox"], line["text"])
                        for line in analysis["analyzeResult"]["readResults"][0]["lines"]]

            for line in lines:
                p = line[0]
                text = line[1]
                output += text
                output += '\n'
                count += 1

    # print(output)

    # chatgpt部分
    # APIキーの設定
    My_Key = "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" ##### 石戸莞楽のchatgptAPIなので悪用厳禁! (石戸莞楽のクレカから使用する分だけ料金が落とされるので、極力使わないこと!)
    openai.api_key = My_Key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": str(output) + "From this coupon transcription, please display the coupons in the order 'Expiration date, Discount amount, Store name, Category' separated by ',' and with no spaces between them."},
            {"role": "system", "content": "The category should be one of the following seven: '飲食, ファッション, イベント, 旅行, ホビー・エンターテイメント, 健康・美容, その他'."},
            {"role": "system", "content": "When returning results, please do not indicate 'Expiration:', 'Discount:', 'Store Name:', or 'Category:'."},
            {"role": "system", "content": "If any of these elements are not mentioned, please leave them as None."},
            {"role": "system", "content": "Do not say anything else."},
            {"role": "system", "content": "Return these contents in Japanese."},
        ],
    )
    coupon_massage = response.choices[0]["message"]["content"].strip()

    # print(coupon_massage)

    # messages = "小谷流温泉,10%割引券,None"
    Date,Discount,Store,Category = coupon_massage.split(',')

    if Date == "None":
        Date = None
    elif Discount == "None":
        Discount = None
    elif Store == "None":
        Store = None
    elif Category == "None":
        Category = None

    coupon_dict = {
        "date":Date,
        "discount":Discount,
        "store":Store,
        "category":Category
    }

    return(coupon_dict)