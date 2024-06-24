import E91_QKD as QKD
import pandas as pd


def create_excel_file(filename):
    columns = ["Test #", "Количество ЭПР пар","Длина итогового ключа", "Длина pure ключа", "Пар в ИК не запутано", "Пар в ИК не запутано, %",
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


def create_combined_excel(filename,testtype):
    # filename = 'Combined_Test_Results.xlsx'
    if testtype=='params':
        columns = ["тест №",
                   "QUBER-ideal", "QUBER-static", "QUBER-dynamic",
                   "len(ИК)-ideal", "len(ИК)-static", "len(ИК)-dynamic",
                   "len(pure ИК)-ideal", "len(pure ИК)-static", "len(pure ИК)-dynamic",
                   "Untngld ИК bits-ideal", "Untngld ИК bits-static", "Untngld ИК bits-dynamic"]
    elif testtype=='length':
        columns = ["тест №",
                   "Количество ЭПР пар",
                   "QUBER-ideal", "QUBER-static", "QUBER-dynamic",
                   "len(ИК)-ideal", "len(ИК)-static", "len(ИК)-dynamic",
                   "len(pure ИК)-ideal", "len(pure ИК)-static", "len(pure ИК)-dynamic",
                   "Untngld ИК bits-ideal", "Untngld ИК bits-static", "Untngld ИК bits-dynamic"]
    combined_df = pd.DataFrame(columns=columns)

    ideal_df = pd.read_excel(f'Test_{testtype}_ideal_results.xlsx')
    static_df = pd.read_excel(f'Test_{testtype}_static_results.xlsx')
    dynamic_df = pd.read_excel(f'Test_{testtype}_dynamic_results.xlsx')

    combined_df["тест №"] = range(len(ideal_df))
    if testtype=='params':
        metrics = [
            ("QUBER", "QUBER-ideal", "QUBER-static", "QUBER-dynamic"),
            ("Длина итогового ключа", "len(ИК)-ideal", "len(ИК)-static", "len(ИК)-dynamic"),
            ("Длина pure ключа", "len(pure ИК)-ideal", "len(pure ИК)-static", "len(pure ИК)-dynamic"),
            ("Пар в ИК не запутано", "Untngld ИК bits-ideal", "Untngld ИК bits-static", "Untngld ИК bits-dynamic")
        ]
    if testtype=='length':
        combined_df["Количество ЭПР пар"] = ideal_df["Количество ЭПР пар"]
        metrics = [
            ("QUBER", "QUBER-ideal", "QUBER-static", "QUBER-dynamic"),
            ("Длина итогового ключа", "len(ИК)-ideal", "len(ИК)-static", "len(ИК)-dynamic"),
            ("Длина pure ключа", "len(pure ИК)-ideal", "len(pure ИК)-static", "len(pure ИК)-dynamic"),
            ("Пар в ИК не запутано", "Untngld ИК bits-ideal", "Untngld ИК bits-static", "Untngld ИК bits-dynamic")
        ]

    for original_col, ideal_col, static_col, dynamic_col in metrics:
        combined_df[ideal_col] = ideal_df[original_col]
        combined_df[static_col] = static_df[original_col]
        combined_df[dynamic_col] = dynamic_df[original_col]

    combined_df.to_excel(filename, index=False)


def test_E91(testtype, n, testname, filename, num_pairs, inter_prob, int_dp, int_dp_range, n_prob, n_dp, n_dp_range):
    create_excel_file(filename)
    for i in range(n):
        print(f'\nТЕСТ {testtype}\t#{i + 1}\n{testname} \n' + '- ' * 13)

        key_length, pure_length, pairs_not_entangled, pairs_not_entangled_pct, quber, md5_hashed_key = QKD.main(
            num_pairs, inter_prob, int_dp, int_dp_range, n_prob, n_dp, n_dp_range)
        if testtype=='length':
            num_pairs+=5;

        append_to_excel(filename, i, num_pairs, key_length, pure_length, pairs_not_entangled,
                        pairs_not_entangled_pct, quber, md5_hashed_key)


def TestSession(testtype):
    n = int(input(f'\nВведите количество итераций для теста типа <<{testtype}>>:\t'))

    if testtype=='length': num_pairs =5
    elif testtype=='params': num_pairs = 1000

    test_E91(testtype, n, 'В ИДЕАЛЬНЫХ УСЛОВИЯХ - БЕЗ ПЕРЕХВАТА, ВЕР. ШУМА = 5%',
                    f'Test_{testtype}_ideal_results.xlsx', num_pairs, 0,
             0, 0, 0.05, 0, 0)
    test_E91(testtype, n, 'CО СТАТИЧЕСКОЙ ВЕРОЯТНОСТЬЮ ПЕРЕХВАТА =10% И  ШУМА =5%',
                    f'Test_{testtype}_static_results.xlsx', num_pairs,
             0.1, 0, 0, 0.05, 0, 0)
    test_E91(testtype, n, 'C ДИНАМИЧЕСКОЙ ВЕРОЯТНОСТЬЮ ПЕРЕХВАТА =10(+5)% И ШУМА =5(+2.5)%',
                    f'Test_{testtype}_dynamic_results.xlsx', num_pairs, 0.1, 1, 0.05, 0.05, 1, 0.025)
    create_combined_excel(f'Combined_Test_Results_{testtype}_{n}reps-2406.xlsx', testtype)


if __name__ == "__main__":
    print('2450\tСоколов Г.А.\tВКР 2024\n' + '-' * 77 +
          '\n\t<< Разработка эмулятора протокола квантового распределения ключей\n'
          '\t\tс использованием парадокса Эйнштейна-Подольского-Розена >>\n' + '-' * 77)
    a = 1
    while (1):
        print(f'\nСЕССИЯ ТЕСТИРОВАНИЯ {a}')
        TestSession('params')
        TestSession('length')
        a += 1
        e = int(input('- ' * 55 + f'\n> > СЕССИЯ ТЕСТИРОВАНИЯ {a-1} УСПЕШНО ЗАВЕРШЕНА'
                                  '\n> > Файлы с результатами сгенерированы в корневой папке'
                                  '\n> > enter 1 to continue, 0 to exit . . . -->\t'))
        if e == 0:
            exit()