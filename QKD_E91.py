import numpy as np
import pandas as pd
import random
from qutip import basis, bell_state
import hashlib

import launcher as L
import probabilities as pb


# Функция для генерации запутанных пар: библиотека qutip
def generate_entangled_pairs(num_pairs):
    psi = bell_state('00')  # Запутанное состояние Белла
    return [{"id": i, "state": psi, "entangled": True} for i in range(num_pairs)]

# Перехват с вероятностью
def interception(pair, inter_prob, dynamic_prob, range_val):
    if dynamic_prob == 1:
        prob = np.random.uniform(inter_prob - range_val/3, inter_prob + range_val)
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
        prob = np.random.uniform(noise_prob - range_val/3, noise_prob+range_val)
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
def generate_trash_key(df):
    matched_bases_df = df[(df["basis equality"] == 0)]
    alice_trash_key = ''.join(map(str, matched_bases_df["Alice value"].values))
    bob_trash_key = ''.join(map(str, matched_bases_df["Bob value"].values))
    return alice_trash_key, bob_trash_key

def binary_to_MD5(binary_string):
    if len(binary_string) < 256:
        print("\n * * * Длина итогового ключа должна быть >= 256 бит, хэширование отменено . . .")
        return "[insufficient length ! ]"
    binary_string = int(binary_string, 2).to_bytes((len(binary_string) + 7) // 8, byteorder='big')
    md5_hash = hashlib.md5()
    md5_hash.update(binary_string)
    hex_result = md5_hash.hexdigest()
    return hex_result

# Основной алгоритм
def qkd_protocol(num_pairs, inter_prob_line, int_dp, int_dp_range, n_prob, n_dp, n_dp_range):
    pairs = generate_entangled_pairs(num_pairs)
    results_df = create_results_dataframe(num_pairs)
    step=0
    for pair in pairs:
        # Проверка индекса step
        if step >= len(inter_prob_line):
            step = len(inter_prob_line) - 1  # Устанавливаем step в последний допустимый индекс
        inter_prob = inter_prob_line[step]
        #print(step, inter_prob)
        interception_flag = interception(pair, inter_prob, int_dp, int_dp_range)
        noise_flag = noise(pair, n_prob, n_dp, n_dp_range)

        alice_basis = random_basis()
        bob_basis = random_basis()

        if alice_basis == bob_basis:
            alice_value = measure_photon(pair, alice_basis)
            bob_value = 1 - alice_value
        else:
            alice_value = random.randint(0, 1)
            bob_value = random.randint(0, 1)

        s_value = verify_bell_inequality(pair)
        step += 1

        record_results(results_df, pair['id'], pair, inter_prob, interception_flag, noise_flag, alice_basis, bob_basis,
                       alice_value,bob_value, s_value)

    return results_df


def console_display(alice_key,pure_key,pairs_not_entangled,pairs_not_entangled_pct,quber, md5_hashed_key):
    if alice_key and len(alice_key) >= 256:
        print(f"Итоговый \"чистый\" ключ:\t\t{alice_key}"
              f"\nДлина итогового ключа:\t\t{len(alice_key)}"
              f"\n{'-'*16}"
              f"\nДлина pure ключа:\t\t\t{len(pure_key)}"
              f"\nПар не запутано:\t\t\t{pairs_not_entangled}"
              f"\n{'-' * 16}\n")

        # print(f" * * * Незапутанных пар в итоговых битах ключа: {pairs_not_entangled_pct}%.")
        # if len(pure_key) / len(alice_key) < 0.75:
        #     print(f" * * * КЛЮЧ НЕ ЯВЛЯЕТСЯ БЕЗОПАСНЫМ.\n"
        # f"{'-'*16}\n")

        print(f"Итоговый MD5-hashed ключ:\t{md5_hashed_key}")
    else:
        print(
            f"Длина итогового чистого ключа недостаточна:\t{len(alice_key) if alice_key else 0}, реинициализируйте протокол")
    if quber < 0.15:
        print(
            f"Присутствие криптоаналитика не обнаружено:\tQUBER = {round(quber * 100, 2)}%\n")
    else:
        if 0.15 <= quber < 0.35:
            print(
                f"QUBER > 15%: {round((quber) * 100, 2)}%, возможно присутствие криптоаналитика.\n")
        else:
            print(
                f"QUBER > 15%: {round((quber) * 100, 2)}%, присутствие криптоаналитика!\n"
                f"\n! ! ! ВНИМАНИЕ! РЕИНИЦИАЛИЗИРУЙТЕ ПРОТОКОЛ! ! !\n")
    print('- ' * 55)


# Основная функция
def main(num_pairs, inter_prob_line, int_dp, int_dp_range, n_prob, n_dp, n_dp_range,model):

    results_df = qkd_protocol(num_pairs, inter_prob_line, int_dp, int_dp_range, n_prob, n_dp, n_dp_range)

    matching_ids = results_df[results_df["basis equality"] == 1]["ID"].values
    bell_results = results_df["Bell result"].values
    count_bell_violation = np.sum(bell_results <= 2)

    alice_key, bob_key, pure_key = generate_secret_key(results_df)
    # alice_trash_key, bob_trash_key = generate_trash_key(results_df)

    if alice_key and len(alice_key) >= 256:
        key_length = len(alice_key)
        pure_length = len(pure_key)
        pairs_not_entangled = key_length - pure_length
        pairs_not_entangled_pct = 100 - round((pure_length / key_length) * 100, 2)
        quber = count_bell_violation / num_pairs
        md5_hashed_key = binary_to_MD5(alice_key)
    else:
        key_length = 0
        pure_length = 0
        pairs_not_entangled = 0
        pairs_not_entangled_pct = 0
        quber = 0
        md5_hashed_key = "[insufficient length ! ]"

    # Сохранение результатов прямого вызова скрипта в Excel
    results_df.to_excel(f"E91_singlescript_result_{model}.xlsx", index=False)

    # вывод в консоль:
    console_display(alice_key,pure_key,pairs_not_entangled,pairs_not_entangled_pct,quber, md5_hashed_key)

    return key_length, pure_length, pairs_not_entangled, pairs_not_entangled_pct, quber, md5_hashed_key

# Функция для создания DataFrame
def create_results_dataframe(num_pairs):
    columns = ["ID", "inter_prob","interception", "noise", "Entangled status", "Alice basis", "Bob basis", "basis equality",
               "Alice value", "Bob value", "Anticorrelation", "Bell result"]
    return pd.DataFrame(index=range(num_pairs), columns=columns)

# Запись результатов в DataFrame
def record_results(df, idx, pair, inter_prob, interception_flag, noise_flag, alice_basis, bob_basis, alice_value, bob_value, s_value):
    df.at[idx, "ID"] = pair['id']
    df.at[idx, "inter_prob"] = inter_prob
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

def Diploma_singletesting(model_name):
    a = 1
    while (1):
        print(f'\n>> DEBUG: dynamic interception 10%, static noise 1%\nТЕСТ {a}\n' + '- ' * 13)
        n = int(input('Введите количество запутанных пар для передачи:\t'))
        models=['Равномерное','Нормальное','Геометрическое','test']
        if model_name=='test':
            model_name=models[int(input('Выберите вероятность:\n1:\tравномерное распределение'
                                 '\n2:\tнормальное распределение'
                                 '\n3:\tГеометрическое распределение\n'))-1]
        if __name__ == "__main__":
            inter_prob_line=pb.Prob_distribution(n,model_name,'cyan','yes')
        else:
            inter_prob_line = pb.Prob_distribution(n, model_name, 'cyan', 'no')
        main(n, inter_prob_line, 1, 0.1, 0.01, 0, 0,model_name)
        a += 1
        e = int(input('- ' * 55 + '\n> > enter 1 to continue, 0 to exit . . . -->\t'))

        if e == 0:
            if __name__ == "__main__":
                exit()
            else:
                L.Diploma_launcher(a)


if __name__ == "__main__":
    L.Header(1)
    print("E91 single test in progress...")
    Diploma_singletesting('test')