import requests

def main():
    url = "https://neolurk.org/wiki/%D0%91%D0%B8%D0%BC%D0%B1%D0%BE%D1%83%D0%BD%D0%B8%D1%82%D0%B0%D0%B7"

    res = requests.get(url)
    print(res.text)



if __name__ == '__main__':
    main()
