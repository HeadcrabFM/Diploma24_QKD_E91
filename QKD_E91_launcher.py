import test
import E91_QKD as QKD

def Header(a):
    if a==1:
        print('\n'+'-' * 77 +'\n2450\tСПбГМТУ\t10.03.01.04\tСоколов Г.А.\tВКР 2024\n' + '-' * 77 +
              '\n\t<< Разработка эмулятора протокола квантового распределения ключей\n'
              '\tс использованием парадокса Эйнштейна-Подольского-Розена >>\n' + '-' * 77+
              f'\n\n\t\t\t{'* \t'*5}\t\t\t\n')

def Outro(a):
    print('\t\t\t> >\t ВЫХОД')
    o=1
    while o!=0 & o!=1:
        o=int(input("Введите 1 для перезапуска программы, 0 для выхода из программы:\t"))
        if o==0:
            Header(1)
            print('Работа программы завершена! Press Enter...')
            input()
            exit()
        elif o==1:
            print('Перезапуск программы...')
            Diploma_launcher(a)
        else:
            print('Введите 0 или 1!')

def Diploma_launcher(a):
    Header(a)
    print('-' * 77+f"\n\t\t\tГ Л А В Н О Е\t\tМ Е Н Ю\n"
          f"\t\t\t> > > Diploma:\t\tL A U N C H\t\t{a}\n"+ '-' * 77)
    menu=int(input('\nВыберите пункт меню:\n'
          '\t\t> >\t1:\tQKD протокол E91 - single_testing\n'
          '\t\t> >\t2:\tЗапуск серии тестов QKD E91 параметров и длины\n'
          '\t\t> >\t3:\tВЫХОД\n'
          '\n\t\t\t> > '))
    print('-' * 77)
    while (menu!=(1|2|3)):
        if menu==1:
            QKD.Diploma_singletesting('test')
        elif menu==2:
            test.Diploma_TestDisplay()
        else: menu=int(input('ВЫБЕРИТЕ ПУНКТ МЕНЮ 1-3!\n'
                             '\n\t\t\t> > '))
    a+=1
    Outro(a)


if __name__ == "__main__":
    a = 1
    Diploma_launcher(a)
