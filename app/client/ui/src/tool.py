def debug(code, massage=''):
    print('In function  '+massage)
    if(code==0):
        print('OK')
    elif(code==1):
        print('Bug need fix')
    elif(code==-1):
        print('Bug does not know why')
    else:
        print('Bug '+str(code)+'th need fix !!!')