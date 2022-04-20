import requests
import io
import urllib

with io.open('static/upload/original_file/1.txt', 'r', encoding='utf-8') as f:
    texts = f.read()

print('len text :',len(texts))
print(texts)

# languagesemantic.org

# url = "https://lst.nectec.or.th/lst_tools/api/neuswath/v1/tokenize"
url = "https://language-semantic.org/lst_tools/api/neuswth/v1/tokenize"
# url = "https://lst.nectec.or.th/lst_tools/api/longan/v1/tokenize"

# datas={'text':'{}'.format(texts),
#             'sep':'',
#             'sentseg':'false'}

datas={'text':'{}'.format(texts)}

headers = {}
arr = []
response = requests.request("POST", url, headers=headers, data=datas)
print(response.text)
# api = response.json()['result']
# print(api)
# arr.append(api)
# for i in api :
#     print(i)
#     arr.append(i)

# print(arr)