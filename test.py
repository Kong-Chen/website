import getpass
import wmi

# 取得目前登入的Windows使用者名稱
username = getpass.getuser()

# 連線WMI服務
wmi_service = wmi.WMI()

# 查詢目前使用者的AD帳戶資訊
query = f"SELECT * FROM Win32_UserAccount WHERE Name = '{username}'"
result = wmi_service.query(query)

# 檢查是否有結果
if len(result) > 0:
    # 取得第一筆結果
    user = result[0]
    print (user)
    # 取得AD帳戶資訊
    domain = user.Domain
    full_name = user.FullName
    sid = user.SID

    # 輸出結果
    #print("使用者名稱: ", username)
    #print("網域: ", domain)
    #print("全名: ", full_name)
    #print("安全識別碼 (SID): ", sid)

else:
    print("找不到使用者帳戶。")
