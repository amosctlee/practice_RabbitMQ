
## tutorial document
https://www.rabbitmq.com/tutorials/tutorial-two-python.html

## 本系列關鍵字
- Consumer Acknowledgements: 
Delivery processing acknowledgements from consumers to RabbitMQ are known as acknowledgements in messaging protocols.
- Publisher Confirms: 
broker acknowledgements to publishers are a protocol extension called publisher confirms.
- durable queue: queue_declare 的時候將durable 設為True，確保queue 本身(不含裡面的訊息)會被RabbitMQ 保存下來。如果是已經存在的queue 則不能改變 durable 設定
- delivery_mode: 設定為 2 表示即使RabbitMQ server restart，訊息也會被保存。
- prefetch_count: 使用basic_qos 來設定，用於平衡多個worker 的負載，避免耗資源的任務因為round-robin 的原因都交給同一個worker

## 實驗一
啟動兩個worker後，開始發送多則訊息到queue中，預設RabbitMQ 會採用round-robin 將任務交派給worker。

worker 會根據message 中句號 "." 的數量來決定sleep的秒數，例如message 中有三個句號，worker 收到message 後會time.sleep(3)

### shell 1
python worker.py

### shell 2
python worker.py

### shell 3
python new_task.py First message.
python new_task.py Second message..
python new_task.py Third message...
python new_task.py Fourth message....
python new_task.py Fifth message.....


## 實驗二
如果任務執行到一半worker 因為某種原因掛了(its channel is closed, connection is closed, or TCP connection is lost)，RabbitMQ 會把訊息重新放進queue中(re-queue)，讓另一個worker 進行處理。

為了讓訊息不要重複被處理，當worker 處理好訊息後要發送ack(nowledgement)給RabbitMQ，讓RabbitMQ 把訊息刪除。

ps. 在實驗一中，因為我們使用 auto_ack=True ，當RabbitMQ 發送訊息給worker 後會立刻刪除訊息。

### 觀察不ack message 的運作方式
把auto_ack=True 註解掉，重複實驗一，然後關閉一個worker 發現訊息被另一個worker 處理了。
```
channel.basic_consume(queue='hello',
                    # auto_ack=True,
                    on_message_callback=callback)
```

### 不要auto_ack，由人工ack 確保訊息有被處理完成
因為沒有auto_ack，所以我們在callback 函式最後加入一行程式碼(如下)，來人工ack。
```
ch.basic_ack(delivery_tag = method.delivery_tag)
```

ps. 要透過同一個channel 來接收與ack message，如果使用不同channel 會造成channel-level protocol exception

## 實驗三
透過人工 ack 訊息，確保任務不會因為auto_ack 丟失，但如果RabbitMQ server 本身掛了，訊息還是會消失。

為了避免以上狀況，我們要主動告訴RabbitMQ 兩件事:  mark both the queue and messages as durable.

1. 設定durable queue
```
channel.queue_declare(queue='task_queue', durable=True)  # 如果是已經存在的queue 則不能改變 durable 設置
```
2. 將message 標記為要保存: delivery_mode = 2
```
channel.basic_publish(exchange='',
                      routing_key="task_queue",
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
``` 

ps. 以上做法不完全保證message 不會丟失，因為在RabbitMQ 收到訊息與儲存訊息之間有短暫的時間差，如果訊息保存非常重要，可以使用 publisher confirms


## 實驗四
目前為止，我們的queue 使用round-robin 在數量上很 '公平' 的分派任務給workers，但有時候每個任務份量是不平均的，有的任務要處理比較久，有的任務處理時間很短，這樣會造成有的worker 很忙碌，有的則被閒置。

我們可以透過channel的basic_qos method，設定 prefetch_count=1，告訴RabbitMQ 在worker ack 前一則訊息前，不要傳送新訊息。
```
channel.basic_qos(prefetch_count=1)
```


## Cut and paste paragraph
The main idea behind Work Queues (aka: Task Queues) is to avoid doing a resource-intensive task immediately and having to wait for it to complete. Instead we schedule the task to be done later. We encapsulate a task as a message and send it to the queue. A worker process running in the background will pop the tasks and eventually execute the job. When you run many workers the tasks will be shared between them.


By default, RabbitMQ will send each message to the next consumer, in sequence. On average every consumer will get the same number of messages. This way of distributing messages is called round-robin. 

