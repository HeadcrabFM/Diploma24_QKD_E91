import numpy as np
import pandas as pd
import random
from qutip import basis, tensor, bell_state


# Функция для генерации запутанных пар
def generate_entangled_pairs(num_pairs):
    psi = bell_state('00')  # Запутанное состояние Белла
    return [{"id": i, "state": psi, "entangled": True} for i in range(num_pairs)]


# Перехват (10% вероятность)
def interception(pair):
    if pair['entangled'] and np.random.random() < 0.1:
        pair['state'] = (random.randint(0, 1), 1 - random.randint(0, 1))
        pair['entangled'] = False
        return True
    return False


# Шум (0.1% вероятность)
def noise(pair):
    if pair['entangled'] and np.random.random() < 0.01:
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


def trim_to_256_bits(binary_string):
    # Оставляем только первые 256 символов и отбрасываем остальные
    binary_string = binary_string[:256]
    return binary_string


def binary_to_hex(binary_string):
    # Убедимся, что длина строки равна 256 битам
    if len(binary_string) != 256:
        raise ValueError("Длина двоичного ключа должна быть 256 бит")

    # Переводим двоичный ключ в десятичное число
    decimal_representation = int(binary_string, 2)

    # Переводим десятичное число в шестнадцатеричное представление
    binary_string = hex(decimal_representation)[2:]  # [2:] для удаления префикса '0x'

    # Убедимся, что шестнадцатеричная строка имеет длину 64 символа (256 бит = 64 шестнадцатеричных цифры)
    binary_string = binary_string.zfill(64)

    return binary_string


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


# Проверка выполнения неравенства Белла
def verify_bell_inequality(pair):
    if pair['entangled']:
        return random.uniform(2, 2 * np.sqrt(2))
    else:
        return random.uniform(0, 2)


# Основной алгоритм
def qkd_protocol(num_pairs):
    pairs = generate_entangled_pairs(num_pairs)
    results_df = create_results_dataframe(num_pairs)

    for pair in pairs:
        interception_flag = interception(pair)
        noise_flag = noise(pair)

        alice_basis = random_basis()
        bob_basis = random_basis()

        if pair['entangled']:
            if alice_basis == bob_basis:
                alice_value = measure_photon(pair, alice_basis)
                bob_value = 1 - alice_value
            else:
                alice_value = random.randint(0, 1)
                bob_value = random.randint(0, 1)
        else:
            alice_value = pair['state'][0]
            bob_value = pair['state'][1]

        s_value = verify_bell_inequality(pair)
        record_results(results_df, pair['id'], pair, interception_flag, noise_flag, alice_basis, bob_basis, alice_value,
                       bob_value, s_value)

    return results_df


# Генерация секретного ключа
def generate_secret_key(df):
    matched_bases_df = df[(df["basis equality"] == 1) & (df["Bell result"] >= 2)]
    alice_key = ''.join(map(str, matched_bases_df["Alice value"].values))
    bob_key = ''.join(map(str, matched_bases_df["Bob value"].values))

    if alice_key == ''.join('1' if x == '0' else '0' for x in bob_key):
        print("Ключи Алисы и Боба инвертны.")
        return alice_key, bob_key
    else:
        print("Ключи Алисы и Боба не инвертны.")
        return alice_key, None

def generate_trash_key(df):
    matched_bases_df = df[(df["basis equality"] == 0)]
    alice_trash_key = ''.join(map(str, matched_bases_df["Alice value"].values))
    bob_trash_key = ''.join(map(str, matched_bases_df["Bob value"].values))
    return alice_trash_key, bob_trash_key

# Расчет QBER
def calculate_qber(alice_key, bob_key, num_pairs):
    errors = sum(1 for a, b in zip(alice_key, bob_key) if a == b)
    return errors / len(alice_key)


# Основная функция
def main():
    num_pairs = 1000
    results_df = qkd_protocol(num_pairs)

    # Вывод ID строк, где базисы совпадают
    matching_ids = results_df[results_df["basis equality"] == 1]["ID"].values
    # print(f"ID строк с совпадающими базисами: {matching_ids}")

    # Анализ графы "Bell result"
    bell_results = results_df["Bell result"].values
    count_bell_violation = np.sum(bell_results <= 2)

    if count_bell_violation / num_pairs < 0.1:
        print(
            f"Присутствие криптоаналитика не обнаружено: {round((count_bell_violation / num_pairs) * 100, 2)}% незапутанных пар")
    else:
        print(
            f"Незапутанных пар больше 10%: {round((count_bell_violation / num_pairs) * 100, 2)}%, возможно присутствие криптоаналитика.")

    # Генерация секретного ключа
    alice_key, bob_key = generate_secret_key(results_df)
    alice_trash_key, bob_trash_key = generate_trash_key(results_df)
    if alice_key and len(alice_key) >= 256:
        print(f"\nИтоговый \"чистый\" ключ:\t{alice_key}\nДлина чистого ключа:\t{len(alice_key)}")
        print(f"Итоговый HEX(16) ключ:\t{binary_to_hex(trim_to_256_bits(alice_key))}\n\n")

        # Расчет QBER
        qber = calculate_qber(alice_trash_key, bob_trash_key,num_pairs)/3
        print(f"QBER: {qber:.2%}")
        if qber > 0.15:
            print("Превышен уровень 15%")
        else:
            print("Уровень ниже 15%")
    else:
        print(
            f"Длина итогового чистого ключа недостаточна:\t{len(alice_key) if alice_key else 0}, реинициализируйте протокол")

    # Сохранение результатов в Excel
    results_df.to_excel("results.xlsx", index=False)


if __name__ == "__main__":
    main()
