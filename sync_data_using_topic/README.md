
## 啟動步驟
1. 啟動rabbitmq container
    ```
    docker-compose up -d rabbitmq
    ```
2. 瀏覽器輸入: http://localhost:15672/ 觀察是否啟動完成
3. 啟動剩下的containers，啟動時build images
    ```
    docker-compose up -d --build
    ```
4. 觀察 subscribers 的log 檔
5. 進入publisher container
    ```
    docker exec -it publisher sh
    ```
6. 在publisher container 內啟動腳本，並開始輸入topic 與要傳送的訊息
   ```
   python publish_tables.py
   ```

