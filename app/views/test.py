
if __name__ == '__main__':
    s = '../static/json/2020/42.json'
    with open(s) as f:
        json_str = f.read()
    print(json_str)