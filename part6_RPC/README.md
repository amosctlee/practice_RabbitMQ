
## tutorial document
https://www.rabbitmq.com/tutorials/tutorial-six-python.html


## key words
- Callback queue: A client sends a request message and a server replies with a response message. In order to receive a response the client needs to send a 'callback' queue address with the request.
- Correlation id: 發送request 時附帶此 id ，用來對應到正確的 RPC server 的回覆訊息


![](https://www.rabbitmq.com/img/tutorials/python-six.png)

## 注意的地方
clien 發送RPC 給server 進行處理，有可能在server 處理完，並將訊息回覆給callback queue 後發生故障，但發生故障的時間點如果在 acknowledgment 之前，則server 可能會再次取得該消息並發送第二的相同correlation id 的訊息到callback queue，因此我們做為client 端，要有適當的措施處理此情況。
