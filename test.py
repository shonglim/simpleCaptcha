from solution import Captcha

if __name__ == '__main__':
    model=Captcha('input','output')

    model('input/input100.jpg','output/output100.txt')
    with open('output/output100.txt','r') as fp:
        lines=fp.readlines()
    print(lines[0])
    