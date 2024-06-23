import QKD
import pandas as pd

def create_excel_file(filename):
    columns = ["Test #", "Длина итогового ключа", "Длина pure ключа", "Пар в ИК не запутано", "Пар в ИК не запутано, %", "QUBER", "MD5-hashed ключ"]
    df = pd.DataFrame(columns=columns)
    df.to_excel(filename, index=False)

def append_to_excel(filename, test_number, key_length, pure_length, pairs_not_entangled, pairs_not_entangled_pct, quber, md5_hashed_key):
    df = pd.read_excel(filename)
    new_row = {
        "Test #": test_number,
        "Длина итогового ключа": key_length,
        "Длина pure ключа": pure_length,
        "Пар в ИК не запутано": pairs_not_entangled,
        "Пар в ИК не запутано, %": pairs_not_entangled_pct,
        "QUBER": quber,
        "MD5-hashed ключ": md5_hashed_key
    }
    df = df._append(new_row, ignore_index=True)
    df.to_excel(filename, index=False)

def create_combined_excel():
    filename = 'Combined_Test_Results.xlsx'
    columns = ["тест №",
               "len(ИК)-ideal","len(ИК)-static","len(ИК)-dynamic",
               "len(pure ИК)-ideal","len(pure ИК)-static","len(pure ИК)-dynamic",
               "Untngld ИК bits-ideal","Untngld ИК bits-static","Untngld ИК bits-dynamic",
               "QUBER-ideal", "QUBER-static", "QUBER-dynamic"]
    combined_df = pd.DataFrame(columns=columns)

    ideal_df = pd.read_excel('Test_ideal_results.xlsx')
    static_df = pd.read_excel('Test_static_results.xlsx')
    dynamic_df = pd.read_excel('Test_dynamic_results.xlsx')

    combined_df["тест №"] = range(1, len(ideal_df) + 1)

    combined_df["len(ИК)-ideal"] = ideal_df["Длина итогового ключа"]
    combined_df["len(ИК)-static"] = static_df["Длина итогового ключа"]
    combined_df["len(ИК)-dynamic"] = dynamic_df["Длина итогового ключа"]

    combined_df["len(pure ИК)-ideal"] = ideal_df["Длина pure ключа"]
    combined_df["len(pure ИК)-static"] = static_df["Длина pure ключа"]
    combined_df["len(pure ИК)-dynamic"] = dynamic_df["Длина pure ключа"]

    combined_df["Untngld ИК bits-ideal"] = ideal_df["Пар в ИК не запутано"]
    combined_df["Untngld ИК bits-static"] = static_df["Пар в ИК не запутано"]
    combined_df["Untngld ИК bits-dynamic"] = dynamic_df["Пар в ИК не запутано"]

    combined_df["QUBER-ideal"] = ideal_df["QUBER"]
    combined_df["QUBER-static"] = static_df["QUBER"]
    combined_df["QUBER-dynamic"] = dynamic_df["QUBER"]

    combined_df.to_excel(filename, index=False)

def test(n,testname,filename,num_pairs, inter_prob, int_dp, int_dp_range, n_prob, n_dp, n_dp_range):
    create_excel_file(filename)
    for i in range(n):
        print(f'\nТЕСТ {testname} #{i + 1}\n' + '- ' * 13)
        key_length, pure_length, pairs_not_entangled, pairs_not_entangled_pct, quber, md5_hashed_key = QKD.main(num_pairs, inter_prob, int_dp, int_dp_range, n_prob, n_dp, n_dp_range)
        append_to_excel(filename, i + 1, key_length, pure_length, pairs_not_entangled, pairs_not_entangled_pct, quber, md5_hashed_key)


test(1000,'В ИДЕАЛЬНЫХ УСЛОВИЯХ - БЕЗ ПЕРЕХВАТА, ВЕР. ШУМА = 5%','Test_ideal_results.xlsx',1000,0,0,0,0.05,0,0)
test(1000,'CО СТАТИЧЕСКОЙ ВЕРОЯТНОСТЬЮ ШУМА =10% И ПЕРЕХВАТА =5%','Test_static_results.xlsx',1000,0.1,0,0,0.05,0,0)
test(1000,'C ДИНАМИЧЕСКОЙ ВЕРОЯТНОСТЬЮ ШУМА =10(+5)% И ПЕРЕХВАТА =5(+2.5)%','Test_dynamic_results.xlsx',1000,0.1,1,0.05,0.05,1,0.025)
create_combined_excel()