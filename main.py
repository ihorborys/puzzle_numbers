# Розроблено за допомогою Python 3 та з підтримкою AI-асистента Google Gemini

import collections
import time


def merge_chain(chain):
    """Збирає фінальний рядок пазла, накладаючи спільні 2 цифри на стиках.

    Приклад: ['248460', '608017', '177092'] -> '24846080177092'
    """
    if not chain:
        return ""
    return chain[0] + "".join(frag[2:] for frag in chain[1:])


def validate_chain(chain, all_fragments):
    """Перевіряє, чи всі стики правильні та чи немає повторного використання фрагментів."""
    for i in range(len(chain) - 1):
        if chain[i][-2:] != chain[i + 1][:2]:
            raise ValueError(
                f"Помилка стику між {chain[i]} та {chain[i+1]} на позиції {i}"
            )

    used_counts = collections.Counter(chain)
    available_counts = collections.Counter(all_fragments)
    for frag, count in used_counts.items():
        if count > available_counts[frag]:
            raise ValueError(
                f"Фрагмент {frag} використано більше разів, ніж є у файлі!"
            )
    return True


def find_longest_puzzle(fragments):
    """Знаходить найдовший однорядний пазл методом пошуку в глибину (DFS) з поверненням."""
    # Залишаємо тільки коректні цифрові фрагменти довжиною від 2 символів
    valid_frags = [
        f.strip()
        for f in fragments
        if f.strip().isdigit() and len(f.strip()) >= 2
    ]
    n = len(valid_frags)

    # Переводимо префікси та суфікси в числа 0..99 для максимальної швидкодії
    prefixes = [int(f[:2]) for f in valid_frags]
    suffixes = [int(f[-2:]) for f in valid_frags]

    # Список суміжності: для кожного префікса (0..99) зберігаємо індекси фрагментів
    adj = [[] for _ in range(100)]
    for idx, pref in enumerate(prefixes):
        adj[pref].append(idx)

    used = [False] * n
    current_chain = []
    best_chain_indices = []

    def dfs(curr_suffix):
        nonlocal best_chain_indices
        if len(current_chain) > len(best_chain_indices):
            best_chain_indices = current_chain.copy()

        for next_idx in adj[curr_suffix]:
            if not used[next_idx]:
                used[next_idx] = True
                current_chain.append(next_idx)

                dfs(suffixes[next_idx])

                current_chain.pop()
                used[next_idx] = False

    # Перевіряємо кожен фрагмент як можливий початок пазла
    for start_idx in range(n):
        used[start_idx] = True
        current_chain.append(start_idx)

        dfs(suffixes[start_idx])

        current_chain.pop()
        used[start_idx] = False

    return [valid_frags[i] for i in best_chain_indices]


if __name__ == "__main__":
    # 1. Самоперевірка на тестовому прикладі з умови задачі
    test_fragments = ["608017", "248460", "962282", "994725", "177092"]
    test_chain = find_longest_puzzle(test_fragments)
    test_answer = merge_chain(test_chain)
    assert (
        test_answer == "24846080177092"
    ), f"Помилка на тесті: {test_answer}"
    print(f"Тест з умови пройдено успішно: {test_answer}\n")

    # 2. Розв'язання задачі для основного файлу
    file_path = "source.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        raw_fragments = file.read().split()

    print(f"Зчитано фрагментів із файлу: {len(raw_fragments)}")

    start_time = time.time()
    best_chain = find_longest_puzzle(raw_fragments)
    elapsed = time.time() - start_time

    # 3. Перевірка правильності ланцюжка та формування відповіді
    validate_chain(best_chain, raw_fragments)
    final_sequence = merge_chain(best_chain)

    print(f"Час пошуку: {elapsed:.2f} с")
    print(f"Кількість фрагментів у найдовшому ланцюжку: {len(best_chain)}")
    print(f"Довжина фінального рядка (символів): {len(final_sequence)}")
    print("\nЛанцюжок фрагментів:")
    print(" & ".join(best_chain))
    print("\nФІНАЛЬНА ПОСЛІДОВНІСТЬ:")
    print(final_sequence)