secret_num = 56
guess = None


while secret_num != guess :
    guess = int(input("輸入數字"))
    if guess > secret_num:
        print("小一點")
    elif guess < secret_num:
        print("大一點")
        
print("恭喜")        