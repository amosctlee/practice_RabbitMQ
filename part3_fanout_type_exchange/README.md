
## tutorial document
https://www.rabbitmq.com/tutorials/tutorial-three-python.html


## key words
- exchange
exchange types: direct, topic, headers, fanout
- binding: the relationship between exchange and queue. describe the rule when exchange dispatch message
- exclusive : a queue's property, used by only one connection and the queue will be deleted when that connection closes
- routing_key: messages are routed to the queue with the name specified by routing_key
- fanout: broadcasts all the messages it receives to all the queues it knows

## 操作重點
1. 宣告一個exchange，exchange_type='fanout'
2. subscriber 宣告一個queue，綁定exchange: channel.queue_bind(exchange='logs', queue=queue_name)
3. 宣告queue 時空字串表示讓系統幫我們隨機取名: channel.queue_declare(queue='', exclusive=True)
4. 由於使用fanout 模式，發送訊息時routing_key 參數會被忽略，在練習中我們輸入空字串

![a exchange binding with two temporary queues](https://www.rabbitmq.com/img/tutorials/python-three-overall.png)