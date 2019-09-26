# 環境資訊 #
- OS：Ubuntu 16.04 LTS
- 預設帳號：詳見 Config 中 machine_config 的 os_user_name 欄位
- 預設密碼：詳見 Config 中 machine_config 的 os_password 欄位
- Python 版本：Python 3
- Hadoop 版本：2.7.3
- Spark 版本：2.0.2
- Hadoop web ui (預設)：master-ip:50070
- Spark web ui(預設)：master-ip:8080
- 最後修改日期：2017/8/27 下午 04:53:54 

----------

# ESXI 範本建立 #
## 預先安裝 OS Package ##
1. `sudo apt-get update`  
2. `sudo apt-get upgrade`  
3. `sudo apt-get install vim ssh openjdk-8-jdk  python3-pip sshpass`  
4. **如果還有其他需要的 Package 請自行安裝**

## 預先安裝 Python3 Library ##
1. `sudo pip3 install django pysolr numppy py4j  jsonpickle django-cors-headers`
2. **如果還有其他需要的 Library 請自行安裝**

## 搬移 Spark Library ##
1. 從 [Spark](https://spark.apache.org/downloads.html "Spark") 下載頁面中下載 Spark 並解壓縮
2. 切換至 Spark 資料夾中
3. 執行 `sudo cp -r python/pyspark /usr/local/lib/python3.x/dist-packages/` ( x 為 Python 3 版本)
4. 複製完後，清除 Spark 資料夾與壓縮包，並透過 ESXI 介面製作成範本，用於製作虛擬機使用

----------

# 注意事項 #
1. `如果.ssh原本存有資料 執行此專案會覆寫` 

----------

# 使用資訊 (以下操作均在 Master 上執行) #

1. 下載 [Spark](https://spark.apache.org/downloads.html "Spark") 並解壓縮至 `~/Documents` 中
2. 更改 Spark 資料夾名稱為 spark
3. 下載 [Hadoop](http://hadoop.apache.org/releases.html "Hadoop") 並解壓縮至 `~/Documents` 中
4. 更改 Hadoop 資料夾名稱為 hadoop
5. 下載此專案並將 Spark_auto_deploy 資料夾放至 `{path}/Documents` 中
6. 根據需求設定 `src/config` 中的設定檔
7. 切換至 `Spark_auto_deploy/src` 中執行 `python3 main.py` 
8. 切換至 `{path}/Documents/spark/conf` 中 把spark-env.sh內容複製到~/.bashrc
9. 執行source ~/.bashrc

----------

# JSON 設定檔 #
切換至 `src/config` 中編輯各項設定檔
## machine_config ##
1. os_user_name：作業系統使用者名稱 (一個ip對一個username)
2. os_user_password：作業系統使用者密碼 (一個ip對一個password)
3. master_hostname：Master 主機名稱
4. client_hostname：Client 主機名稱 (一個ip對一個主機名稱)
5. client_name_prefix：Spark client 前贅詞，用於 hosts 中
6. local_tar_files_folder_path：將檔案壓縮後暫存的位置中
7. 設定檔中 `master 跟 worker 路徑要一模一樣`
   如果master路徑是 /home/user1/Documents, worker也要是 /home/user1/Documents


## framework_config ##
1. framework_folder_root_path：Hadoop、Spark framework 存放位置
2. JAVA_HOME：JAVA 位置 (盡量將 OS 版本一致，因為路徑才會相同)
3. PYTHON_VERSION：Python 版本
4. PYTHONHASHSEED：Python HASH 的種子


## hadoop_config ##
1. hadoop_folder_name：Hadoop 資料夾名稱
2. hadoop_tar_name：Hadoop 壓縮後的檔案名稱
## spark_config ##
1. spark_master_ip：Spark 的 Master 主機 IP
2. spark_folder_name：Spark 資料夾名稱
3. spark_tar_name：Spark 壓縮後的檔案名稱
4. SPARK_MASTER_MEMORY：Spark Master 記憶體使用
5. SPARK_DRIVER_MEMORY：Spark Driver 記憶體使用
6. SPARK_WORKER_MEMORY：Spark Worker 記憶體使用
7. SPARK_EXECUTOR_MEMORY：Spark Executor 記憶體使用
8. SPARK_WORKER_CORES：Spark Work CPU core 使用


## test_config ##
1. test_machines_ip_list：測試用佈署主機 IP 清單


## ip_list ##
1. machines_ip_list：實際佈署主機 IP 清單

