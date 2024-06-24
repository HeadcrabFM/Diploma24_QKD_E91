import test
import E91_QKD as QKD

def Header(a):
    if a==1:
        print('\n2450\tСПбГМТУ\t10.03.01.04\tСоколов Г.А.\tВКР 2024\n\n' + '-' * 77 +
              '\n\t<< Разработка эмулятора протокола квантового распределения ключей\n'
              '\tс использованием парадокса Эйнштейна-Подольского-Розена >>\n' + '-' * 77)

def Outro():
    while o==0 | o==1:
        o=int(input("Введите 1 для перезапуска программы, любюую другую цифру для выхода из программы:"))
        if o==0:
            print('Работа программы завершена! Press Enter...')
            input()
            exit()
        else:
            pass

def Diploma_launcher(a):
    Header(a)
    print('-' * 77+f"\n\t\t\tГ Л А В Н О Е\t\tМ Е Н Ю\n"
          f"\t\t\t> > > Diploma:\t\tL A U N C H\t{a}\n"+ '-' * 77)
    menu=int(input('\nВыберите пункт меню:\n'
          '\t\t> > 1:\tQKD протокол E91 - single_testing\n'
          '\t\t> > 2:\tЗапуск серии тестов QKD E91 параметров и длины\n\n\t\t\t> > '))
    print('-' * 77)
    if menu==1:
        QKD.Diploma_singletesting()
    elif menu==2:
        test.Diploma_TestDisplay()
    Outro()
    a+=1

if __name__ == "__main__":
    a = 1
    Diploma_launcher(a)