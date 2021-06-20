
## tutorial document
https://www.rabbitmq.com/tutorials/tutorial-five-python.html


## key words
- topic exchange: Messages sent to a topic exchange can't have an arbitrary routing_key - it must be a list of words, delimited by dots. (ex: "stock.usd.nyse", "nyse.vmw", "quick.orange.rabbit")

## 重要概念
1. topic exchange 與 direct exchange 很像，同樣會把訊息傳送給binding key 與指定的routing key 相同的 queue，然而他們之間的不同在於topic exchange 支援萬用字元:
    - \* (star) can substitute for exactly one word.
    - \# (hash) can substitute for zero or more words.
    
    如下圖: ![](https://www.rabbitmq.com/img/tutorials/python-five.png)

2. 如果routing key 的單字數(以.分隔)與binding key 的單字數不同，則不會match，例如: 'quick.orange.male.rabbit' 不會傳送到上圖任一queue，但 'lazy.orange.male.rabbit' 會傳送給第二個queue，因為#字號代表任意單字數

