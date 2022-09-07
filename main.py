from house import parse
from views import write_csv, get_house

def main():
    choise = input('input:\n1 - parse houses:\n2 - write all data from db to csv file:\n')
    
    if choise == '1':
        parse()
        
    elif choise == '2':    
        write_csv(get_house())
        
if __name__ == '__main__':
    main()


