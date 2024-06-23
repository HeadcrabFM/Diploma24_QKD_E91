import numpy as np
import pandas as pd
import random
from qutip import basis, bell_state
import hashlib


# Создание DataFrame для хранения результатов
def create_results_dataframe(num_pairs):
    columns = ["ID", "interception", "noise", "Entangled status", "Alice basis", "Bob basis", "basis equality",
               "Alice value", "Bob value", "Anticorrelation", "Bell result"]
    return pd.DataFrame(index=range(num_pairs), columns=columns)


# Запись результатов в DataFrame
def record_results(df, idx, pair, interception_flag, noise_flag, alice_basis, bob_basis, alice_value, bob_value,
                   s_value):
    df.at[idx, "ID"] = pair['id']
    df.at[idx, "interception"] = int(interception_flag)
    df.at[idx, "noise"] = int(noise_flag)
    df.at[idx, "Entangled status"] = int(pair['entangled'])
    df.at[idx, "Alice basis"] = alice_basis
    df.at[idx, "Bob basis"] = bob_basis
    df.at[idx, "basis equality"] = int(alice_basis == bob_basis)
    df.at[idx, "Alice value"] = alice_value
    df.at[idx, "Bob value"] = bob_value
    df.at[idx, "Anticorrelation"] = int(alice_value != bob_value)
    df.at[idx, "Bell result"] = s_value


# Функция для генерации запутанных пар: библиотека qutip
def generate_entangled_pairs(num_pairs):
    psi = bell_state('00')  # Запутанное состояние Белла
    return [{"id": i, "state": psi, "entangled": True} for i in range(num_pairs)]


# Перехват с вероятностью
def interception(pair, inter_prob, dynamic_prob, range_val):
    if dynamic_prob == 1:
        prob = np.random.uniform(inter_prob - range_val, inter_prob)
    else:
        prob = inter_prob

    if pair['entangled'] and np.random.random() < prob:
        pair['state'] = (random.randint(0, 1), 1 - random.randint(0, 1))
        pair['entangled'] = False
        return True
    return False


# Шум с вероятностью
def noise(pair, noise_prob, dynamic_prob, range_val):
    if dynamic_prob == 1:
        prob = np.random.uniform(noise_prob - range_val, noise_prob)
    else:
        prob = noise_prob

    if pair['entangled'] and np.random.random() < prob:
        pair['state'] = (random.randint(0, 1), 1 - random.randint(0, 1))
        pair['entangled'] = False
        return True
    return False


# Случайный выбор базиса
def random_basis():
    bases = ['linear', 'diagonal', 'circular']
    return random.choice(bases)


# Измерение состояния в выбранном базисе
def measure_photon(pair, basis):
    if pair['entangled']:
        result = 0 if random.random() < 0.5 else 1
        pair['state'] = (result, 1 - result)
    return pair['state'][0]


# Проверка выполнения неравенства Белла
def verify_bell_inequality(pair):
    if pair['entangled']:
        return random.uniform(2, 2 * np.sqrt(2))
    else:
        return random.uniform(0, 2)


# Генерация секретного ключа
def generate_secret_key(df):
    matched_bases_df = df[(df["basis equality"] == 1)]
    purest_df = df[(df["basis equality"] == 1) & (df["Bell result"] >= 2)]
    alice_key = ''.join(map(str, matched_bases_df["Alice value"].values))
    bob_key = ''.join(map(str, matched_bases_df["Bob value"].values))
    pure_key = ''.join(map(str, purest_df["Alice value"].values))
    print('\nA_key:\t', alice_key)
    print('B_key:\t', bob_key)

    if alice_key == ''.join('1' if x == '0' else '0' for x in bob_key):
        print("Ключи Алисы и Боба инвертны\n")
        return alice_key, bob_key, pure_key
    else:
        print("Ключи Алисы и Боба НЕ инвертны!\n"
              "ОШИБКА РАБОТЫ ПРОТОКОЛА!\n")
        return alice_key, None, pure_key


# хранение отброшенных ключей
# для возможности последующих использований
# ругих методов проверки и постобработки
def generate_trash_key(df):
    matched_bases_df = df[(df["basis equality"] == 0)]
    alice_trash_key = ''.join(map(str, matched_bases_df["Alice value"].values))
    bob_trash_key = ''.join(map(str, matched_bases_df["Bob value"].values))
    return alice_trash_key, bob_trash_key


def binary_to_hex(binary_string):
    if len(binary_string) < 256:
        #raise ValueError("Длина двоичного ключа должна быть >= 256 бит")
        print("\n * * * Длина итогового ключа должна быть >= 256 бит, хэширование отменено . . .")
        return "[insufficient length ! ]"
    binary_string = int(binary_string, 2).to_bytes((len(binary_string) + 7) // 8, byteorder='big')
    md5_hash = hashlib.md5()
    md5_hash.update(binary_string)
    hex_result = md5_hash.hexdigest()
    return hex_result


# Основной алгоритм
def qkd_protocol(num_pairs,inter_prob,int_dp,int_dp_range,n_prob,n_dp,n_dp_range):
    pairs = generate_entangled_pairs(num_pairs)
    results_df = create_results_dataframe(num_pairs)

    for pair in pairs:
        interception_flag = interception(pair, inter_prob,int_dp,int_dp_range)
        noise_flag = noise(pair, n_prob,n_dp,n_dp_range)

        alice_basis = random_basis()
        bob_basis = random_basis()

        if alice_basis == bob_basis:
            alice_value = measure_photon(pair, alice_basis)
            bob_value = 1 - alice_value
        else:
            alice_value = random.randint(0, 1)
            bob_value = random.randint(0, 1)

        s_value = verify_bell_inequality(pair)
        record_results(results_df, pair['id'], pair, interception_flag, noise_flag, alice_basis, bob_basis, alice_value,
                       bob_value, s_value)

    return results_df


# Основная функция
def main(num_pairs, inter_prob,int_dp,int_dp_range,n_prob,n_dp,n_dp_range):
    results_df = qkd_protocol(num_pairs,inter_prob,int_dp,int_dp_range,n_prob,n_dp,n_dp_range)

    # Вывод ID строк, где базисы совпадают, для консольной проверки
    matching_ids = results_df[results_df["basis equality"] == 1]["ID"].values
    #print(f"ID строк с совпадающими базисами:\n{matching_ids}")

    # Анализ графы результатов теста"Bell result"
    bell_results = results_df["Bell result"].values
    count_bell_violation = np.sum(bell_results <= 2)

    # Генерация секретного ключа
    alice_key, bob_key, pure_key = generate_secret_key(results_df)
    # alice_trash_key, bob_trash_key = generate_trash_key(results_df)

    if alice_key and len(alice_key) >= 256:
        print(f"Итоговый \"чистый\" ключ:\t\t{alice_key}"
              f"\nДлина итогового ключа:\t\t{len(alice_key)}"
              f"\n{'-'*16}"
              f"\nДлина pure ключа:\t\t\t{len(pure_key)}"
              f"\nПар не запутано:\t\t\t{len(alice_key) - len(pure_key)}"
              f"\n{'-' * 16}\n")
        # print(f" * * * Незапутанных пар в итоговых битах ключа: {100 - round(len(pure_key) / len(alice_key), 2) * 100}%.")
        # if len(pure_key) / len(alice_key) < 0.75:
        #     print(f" * * * КЛЮЧ НЕ ЯВЛЯЕТСЯ БЕЗОПАСНЫМ.\n"
        # f"{'-'*16}\n")
        print(f"Итоговый MD5-hashed ключ:\t{binary_to_hex(alice_key)}")
    else:
        print(
            f"Длина итогового чистого ключа недостаточна:\t{len(alice_key) if alice_key else 0}, реинициализируйте протокол")

    # Расчет QBER
    if count_bell_violation / num_pairs < 0.15:
        print(
            f"Присутствие криптоаналитика не обнаружено:\tQUBER = {round((count_bell_violation / num_pairs) * 100, 2)}%\n")
    else:
        if 0.15 <= count_bell_violation / num_pairs < 0.35:
            print(
                f"QUBER > 15%: {round((count_bell_violation / num_pairs) * 100, 2)}%, возможно присутствие криптоаналитика.\n")
        else:
            print(
                f"QUBER > 15%: {round((count_bell_violation / num_pairs) * 100, 2)}%, присутствие криптоаналитика!\n"
                f"\n! ! ! ВНИМАНИЕ! РЕИНИЦИАЛИЗИРУЙТЕ ПРОТОКОЛ! ! !\n")

    print('- ' * 55)

    # Сохранение результатов в Excel
    results_df.to_excel("results.xlsx", index=False)

# Основной цикл скрипта при прямом обращении
if __name__ == "__main__":
    a = 1
    while (1):
        print(f'\nТЕСТ {a}\n' + '- ' * 8)
        n = int(input('Введите количество запутанных пар для передачи:\t'))
        main(n,0.15,1,0.1,0.01,0,0)
        a += 1
