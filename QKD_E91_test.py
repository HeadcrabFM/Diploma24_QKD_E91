import QKD_E91 as QKD
import QKD_E91_launcher as L
import pandas as pd
import QKD_E91_probabilities as pb
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


def create_excel_file(filename):
    columns = ["Test #", "Количество ЭПР пар", "Длина итогового ключа", "Длина pure ключа", "Пар в ИК не запутано",
               "Пар в ИК не запутано, %",
               "QUBER", "MD5-hashed ключ"]
    df = pd.DataFrame(columns=columns)
    df.to_excel(filename, index=False)


def append_to_excel(filename, test_number, num_pairs, key_length, pure_length, pairs_not_entangled,
                    pairs_not_entangled_pct, quber, md5_hashed_key):
    df = pd.read_excel(filename)
    new_row = {
        "Test #": test_number,
        "Количество ЭПР пар": num_pairs,
        "Длина итогового ключа": key_length,
        "Длина pure ключа": pure_length,
        "Пар в ИК не запутано": pairs_not_entangled,
        "Пар в ИК не запутано, %": pairs_not_entangled_pct,
        "QUBER": quber,
        "MD5-hashed ключ": md5_hashed_key
    }
    df = df._append(new_row, ignore_index=True)
    df.to_excel(filename, index=False)


def create_combined_excel(filename, testtype):
    # filename = 'Combined_Test_Results.xlsx'
    if testtype == 'params':
        columns = ["тест №",
                   "QUBER-uni", "QUBER-normal", "QUBER-geo",
                   "len(ИК)-uni", "len(ИК)-normal", "len(ИК)-geo",
                   "len(pure ИК)-uni", "len(pure ИК)-normal", "len(pure ИК)-geo",
                   "Untngld ИК bits-uni", "Untngld ИК bits-normal", "Untngld ИК bits-geo"]
    elif testtype == 'length':
        columns = ["тест №",
                   "Количество ЭПР пар",
                   "len(ИК)-uni", "len(ИК)-normal", "len(ИК)-geo",
                   "len(pure ИК)-uni", "len(pure ИК)-normal", "len(pure ИК)-geo",
                   "Untngld ИК bits-uni", "Untngld ИК bits-normal", "Untngld ИК bits-geo"]
    combined_df = pd.DataFrame(columns=columns)

    ideal_df = pd.read_excel(f'Равномерное_Test_{testtype}_results.xlsx')
    static_df = pd.read_excel(f'Нормальное_Test_{testtype}_results.xlsx')
    dynamic_df = pd.read_excel(f'Геометрическое_Test_{testtype}_results.xlsx')

    combined_df["тест №"] = range(len(ideal_df))
    if testtype == 'params':
        metrics = [
            ("QUBER", "QUBER-uni", "QUBER-normal", "QUBER-geo"),
            ("Длина итогового ключа", "len(ИК)-uni", "len(ИК)-normal", "len(ИК)-geo"),
            ("Длина pure ключа", "len(pure ИК)-uni", "len(pure ИК)-normal", "len(pure ИК)-geo"),
            ("Пар в ИК не запутано", "Untngld ИК bits-uni", "Untngld ИК bits-normal", "Untngld ИК bits-geo")
        ]
    if testtype == 'length':
        combined_df["Количество ЭПР пар"] = ideal_df["Количество ЭПР пар"]
        metrics = [
            ("Длина итогового ключа", "len(ИК)-uni", "len(ИК)-normal", "len(ИК)-geo"),
            ("Длина pure ключа", "len(pure ИК)-uni", "len(pure ИК)-normal", "len(pure ИК)-geo"),
            ("Пар в ИК не запутано", "Untngld ИК bits-uni", "Untngld ИК bits-normal", "Untngld ИК bits-geo"),
            ("QUBER", "QUBER-uni", "QUBER-normal", "QUBER-geo")
        ]

    for original_col, ideal_col, static_col, dynamic_col in metrics:
        combined_df[ideal_col] = ideal_df[original_col]
        combined_df[static_col] = static_df[original_col]
        combined_df[dynamic_col] = dynamic_df[original_col]

    combined_df.to_excel(filename, index=False)


def test_E91(testtype, n, testname, filename1, num_pairs, int_dp, int_dp_range, n_prob, n_dp, n_dp_range):
    models = ['Равномерное', 'Нормальное', 'Геометрическое']
    # colors=['grey','cyan','pink']
    for i in range(len(models)):
        filename = filename1
        filename = models[i] + '_' + filename
        create_excel_file(filename)
        if __name__ != "__main__":
            # генерация единого ряда вероятностей для серии:
            inter_prob_line = pb.Prob_distribution(num_pairs, models[i], pb.get_random_color(), 'yes')
        if testtype == 'length':
            num_pairs = 250
        for j in range(n):
            print(f'\nТЕСТ {testtype}\t#{i + 1}.{j + 1}\n{testname} - {models[i]} распределение\n' + '- ' * 13)
            if __name__ == "__main__":
                # генерация ряда вероятностей каждую итерацию серии без вывода графика при прямом вызове скрипта:
                inter_prob_line = pb.Prob_distribution(num_pairs, models[i], pb.get_random_color(), 'no')
                print(f'// unique probability line generated... ChartDisplaying is off due to direct script call\n')

            key_length, pure_length, pairs_not_entangled, pairs_not_entangled_pct, quber, md5_hashed_key = QKD.main(
                num_pairs, inter_prob_line, int_dp, int_dp_range, n_prob, n_dp, n_dp_range, models[i])

            if testtype == 'length':
                num_pairs += 2;

            append_to_excel(filename, j, num_pairs, key_length, pure_length, pairs_not_entangled,
                            pairs_not_entangled_pct, quber, md5_hashed_key)


def TestSession(testtype):
    n = int(input(f'\nВведите количество итераций для теста типа <<{testtype}>>:\t'))

    if testtype == 'length':
        num_pairs = n
    elif testtype == 'params':
        num_pairs = 1000

    test_E91(testtype, n, f'ДИНАМИЧЕСКАЯ ВЕРОЯТНОСТЬ',
             f'Test_{testtype}_results.xlsx', num_pairs,
             0, 0, 0.05, 0, 0)
    if __name__ == "__main__":
        testtype.join('_direct')
    create_combined_excel(f'Combined_Test_Results_{testtype}_{n}reps.xlsx', testtype)


def Diploma_TestDisplay():
    a = 1
    while (1):
        print(f'\nСЕССИЯ ТЕСТИРОВАНИЯ ПАРАМЕТРОВ И ДЛИНЫ Е91 №{a}')
        TestSession('params')
        TestSession('length')
        a += 1
        e = int(input('- ' * 55 + f'\n> > СЕССИЯ ТЕСТИРОВАНИЯ {a - 1} УСПЕШНО ЗАВЕРШЕНА'
                                  '\n> > Файлы с результатами сгенерированы в корневой папке'
                                  '\n> > enter 1 to continue, 0 to exit . . . -->\t'))
        if e == 0:
            if __name__ == "__main__":
                exit()
            else:
                L.Diploma_launcher(a)


if __name__ == "__main__":
    L.Header(1)
    Diploma_TestDisplay()
