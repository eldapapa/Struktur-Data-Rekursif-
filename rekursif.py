"""
=============================================================
  TUGAS REKURSIF - ALGORITMA BACKTRACKING
  Berisi 3 program:
    1. N-Queens (N-Ratu)
    2. Knight's Tour (Tur Kuda)
    3. Knapsack Problem
=============================================================
"""

# ============================================================
# SOAL 1: N-QUEENS (N-RATU)
# ============================================================
"""
Deskripsi:
  Tempatkan N ratu di papan catur N×N sehingga tidak ada dua
  ratu yang saling menyerang (tidak sebaris, sekolom, sediagonal).

Pendekatan:
  Backtracking rekursif - coba letakkan ratu kolom per kolom
  di setiap baris. Jika posisi aman, lanjut ke baris berikutnya.
  Jika tidak ada posisi aman, mundur (backtrack) ke baris sebelumnya.
"""

def is_safe_queen(board, row, col, n):
    """
    Memeriksa apakah posisi (row, col) aman untuk meletakkan ratu.
    
    Parameter:
      board : list[int] - board[r] = kolom tempat ratu di baris r
      row   : int       - baris yang sedang dicek
      col   : int       - kolom yang sedang dicek
      n     : int       - ukuran papan
    
    Cek 3 kondisi konflik:
      1. Kolom yang sama sudah ada ratu
      2. Diagonal kiri atas sudah ada ratu
      3. Diagonal kanan atas sudah ada ratu
    """
    for r in range(row):
        c = board[r]
        if c == col:                          # kolom sama
            return False
        if abs(c - col) == abs(r - row):      # sediagonal
            return False
    return True


def solve_nqueens(board, row, n, solutions):
    """
    Fungsi rekursif utama N-Queens.
    
    Parameter:
      board     : list[int] - posisi ratu di setiap baris
      row       : int       - baris yang sedang diproses
      n         : int       - ukuran papan
      solutions : list      - daftar semua solusi yang ditemukan
    
    Basis rekursi:
      row == n → semua ratu berhasil diletakkan, simpan solusi

    Langkah rekursif:
      Coba setiap kolom (0..n-1) di baris 'row'.
      Jika aman → letakkan ratu → rekursi ke baris berikutnya
      Jika kembali → hapus ratu (backtrack) → coba kolom lain
    """
    # Basis: semua baris sudah terisi → solusi ditemukan
    if row == n:
        solutions.append(board[:])  # simpan salinan solusi
        return

    # Coba setiap kolom untuk baris ini
    for col in range(n):
        if is_safe_queen(board, row, col, n):
            board[row] = col            # letakkan ratu
            solve_nqueens(board, row + 1, n, solutions)  # rekursi
            board[row] = -1             # backtrack: hapus ratu


def print_nqueens_board(solution, n):
    """Mencetak papan dalam format visual."""
    separator = "+" + ("---+" * n)
    print(separator)
    for row in range(n):
        row_str = "|"
        for col in range(n):
            if solution[row] == col:
                row_str += " Q |"
            else:
                row_str += " . |"
        print(row_str)
        print(separator)


def run_nqueens():
    """Program utama N-Queens."""
    print("=" * 50)
    print("          PROGRAM N-QUEENS (N-RATU)")
    print("=" * 50)

    # Input dari pengguna
    while True:
        try:
            n = int(input("Masukkan ukuran papan N (N >= 4): "))
            if n >= 1:
                break
            print("N harus >= 1!")
        except ValueError:
            print("Input tidak valid, masukkan angka.")

    # Inisialisasi board dan cari semua solusi
    board = [-1] * n        # board[r] = kolom ratu di baris r (-1 = kosong)
    solutions = []
    solve_nqueens(board, 0, n, solutions)

    # Output hasil
    if not solutions:
        print(f"\nTidak ada solusi untuk N={n}.")
    else:
        print(f"\nDitemukan {len(solutions)} solusi untuk N={n}.\n")
        tampilkan = input(f"Tampilkan semua solusi? (y/n): ").strip().lower()

        for i, sol in enumerate(solutions):
            if tampilkan != 'y' and i >= 3:
                print(f"... dan {len(solutions) - 3} solusi lainnya.")
                break
            print(f"\n--- Solusi {i + 1} ---")
            print_nqueens_board(sol, n)
            # Tampilkan juga dalam format baris-kolom
            posisi = [f"Baris {r+1} → Kolom {sol[r]+1}" for r in range(n)]
            print("Posisi ratu:", ", ".join(posisi))

    print()


# ============================================================
# SOAL 2: KNIGHT'S TOUR (TUR KUDA)
# ============================================================
"""
Deskripsi:
  Kuda catur harus mengunjungi setiap petak di papan N×N
  tepat satu kali, dimulai dari posisi yang ditentukan pengguna.

Pendekatan:
  Backtracking rekursif + Warnsdorff's Heuristic.
  Heuristik: di setiap langkah, pilih petak dengan jumlah
  langkah lanjutan paling sedikit (degree terkecil).
  Ini sangat mengurangi jumlah backtracking.

Langkah legal kuda (8 arah pola L):
  (-2,-1), (-2,+1), (-1,-2), (-1,+2),
  (+1,-2), (+1,+2), (+2,-1), (+2,+1)
"""

# 8 kemungkinan langkah kuda (delta_baris, delta_kolom)
KNIGHT_MOVES = [
    (-2, -1), (-2, +1),
    (-1, -2), (-1, +2),
    (+1, -2), (+1, +2),
    (+2, -1), (+2, +1)
]


def get_valid_moves(board, row, col, n):
    """
    Mengembalikan daftar langkah valid dari posisi (row, col).
    Langkah valid = masih di dalam papan dan belum dikunjungi.
    """
    moves = []
    for dr, dc in KNIGHT_MOVES:
        nr, nc = row + dr, col + dc
        if 0 <= nr < n and 0 <= nc < n and board[nr][nc] == -1:
            moves.append((nr, nc))
    return moves


def get_degree(board, row, col, n):
    """
    Menghitung degree (jumlah langkah lanjutan) dari posisi (row, col).
    Digunakan oleh heuristik Warnsdorff.
    """
    return len(get_valid_moves(board, row, col, n))


def solve_knights_tour(board, row, col, move_num, n, path):
    """
    Fungsi rekursif utama Knight's Tour.

    Parameter:
      board    : list[list[int]] - papan, board[r][c] = urutan langkah
      row, col : int             - posisi kuda saat ini
      move_num : int             - nomor langkah berikutnya (mulai dari 1)
      n        : int             - ukuran papan
      path     : list[tuple]     - urutan koordinat yang dikunjungi

    Basis rekursi:
      move_num == n*n → semua petak sudah dikunjungi → True

    Langkah rekursif:
      Ambil semua langkah valid dari posisi saat ini.
      Urutkan berdasarkan degree terkecil (Warnsdorff).
      Coba satu per satu secara rekursif.
      Jika gagal → backtrack (hapus langkah, coba yang lain).
    """
    # Basis: semua n*n petak telah dikunjungi
    if move_num == n * n:
        return True

    # Dapatkan semua langkah valid dan urutkan (Warnsdorff)
    next_moves = get_valid_moves(board, row, col, n)
    # Sortir: prioritaskan petak dengan degree TERKECIL
    next_moves.sort(key=lambda pos: get_degree(board, pos[0], pos[1], n))

    for nr, nc in next_moves:
        board[nr][nc] = move_num    # kunjungi petak
        path.append((nr, nc))

        # Rekursi ke langkah berikutnya
        if solve_knights_tour(board, nr, nc, move_num + 1, n, path):
            return True             # solusi ditemukan

        # Backtrack: batalkan langkah
        board[nr][nc] = -1
        path.pop()

    return False    # tidak ada langkah valid → backtrack


def print_knights_board(board, n):
    """Mencetak papan Tur Kuda dengan nomor urut kunjungan."""
    # Tentukan lebar kolom
    width = len(str(n * n))
    separator = "+" + (("-" * (width + 2) + "+") * n)
    print(separator)
    for r in range(n):
        row_str = "|"
        for c in range(n):
            row_str += f" {board[r][c]+1:>{width}} |"
        print(row_str)
        print(separator)


def print_knights_path(path, n):
    """Mencetak daftar langkah dalam format teks."""
    print("\nDaftar langkah (baris, kolom berbasis 1):")
    for i, (r, c) in enumerate(path):
        label = f"Langkah {i+1:>3}: ({r+1}, {c+1})"
        # Cetak 3 langkah per baris
        end = "\n" if (i + 1) % 3 == 0 or i == len(path) - 1 else "   "
        print(label, end=end)
    print()


def run_knights_tour():
    """Program utama Knight's Tour."""
    print("=" * 50)
    print("        PROGRAM TUR KUDA (KNIGHT'S TOUR)")
    print("=" * 50)

    # Input ukuran papan
    while True:
        try:
            n = int(input("Masukkan ukuran papan N (N >= 5): "))
            if n >= 5:
                break
            print("N minimal 5 untuk memastikan solusi ada!")
        except ValueError:
            print("Input tidak valid.")

    # Input posisi awal
    print(f"Papan {n}×{n}, koordinat dari (1,1) sampai ({n},{n}).")
    while True:
        try:
            start_r = int(input(f"Posisi awal - Baris (1-{n}): ")) - 1
            start_c = int(input(f"Posisi awal - Kolom (1-{n}): ")) - 1
            if 0 <= start_r < n and 0 <= start_c < n:
                break
            print(f"Posisi harus antara 1 dan {n}!")
        except ValueError:
            print("Input tidak valid.")

    # Inisialisasi papan
    board = [[-1] * n for _ in range(n)]
    board[start_r][start_c] = 0     # langkah pertama = 0
    path = [(start_r, start_c)]

    print(f"\nMencari solusi dari posisi ({start_r+1}, {start_c+1})...")

    # Cari solusi
    found = solve_knights_tour(board, start_r, start_c, 1, n, path)

    # Output hasil
    if found:
        print(f"\n✓ SOLUSI DITEMUKAN! Kuda mengunjungi {n*n} petak.\n")
        print("Papan (angka = urutan kunjungan):")
        print_knights_board(board, n)
        print_knights_path(path, n)
    else:
        print("\n✗ Tidak ditemukan solusi dari posisi tersebut.")
        print("Coba posisi awal yang berbeda.")

    print()


# ============================================================
# SOAL 3: KNAPSACK PROBLEM
# ============================================================
"""
Deskripsi:
  Diberikan daftar barang dengan berat masing-masing dan sebuah
  berat target. Cari kombinasi barang yang totalnya TEPAT = target
  (atau tidak melebihi target jika menggunakan versi <=).

Pendekatan:
  Pohon rekursi binary: setiap barang punya 2 pilihan:
    - MASUKKAN: kurangi sisa kapasitas, lanjut ke barang berikutnya
    - LEWATI : lanjut ke barang berikutnya tanpa mengubah kapasitas

  Basis rekursi:
    - sisa == 0        → solusi tepat ditemukan
    - index habis atau sisa < 0 → gagal, backtrack

  Versi 1: exact_knapsack  → cari kombinasi tepat = target
  Versi 2: bounded_knapsack → cari kombinasi terbaik <= target
"""

def exact_knapsack(items, index, remaining, chosen, solutions, max_sols=50):
    """
    Mencari kombinasi barang yang totalnya TEPAT = target.

    Parameter:
      items     : list[int]  - daftar berat semua barang
      index     : int        - indeks barang yang sedang dipertimbangkan
      remaining : int        - sisa kapasitas yang masih dibutuhkan
      chosen    : list[int]  - barang yang sudah dipilih saat ini
      solutions : list       - semua solusi yang ditemukan
      max_sols  : int        - batas maksimum solusi (agar tidak terlalu lama)
    """
    # Basis 1: total tepat sama dengan target → solusi ditemukan
    if remaining == 0:
        solutions.append(chosen[:])
        return

    # Basis 2: barang habis atau sisa negatif → tidak ada solusi di cabang ini
    if index >= len(items) or remaining < 0:
        return

    # Batas: sudah cukup banyak solusi
    if len(solutions) >= max_sols:
        return

    # Pruning: lewati barang yang beratnya > sisa (tidak mungkin valid)
    # (opsional, hanya berlaku jika items terurut)

    # Pilihan 1: MASUKKAN barang ke-index
    chosen.append(items[index])
    exact_knapsack(items, index + 1, remaining - items[index], chosen, solutions, max_sols)
    chosen.pop()                        # backtrack

    # Pilihan 2: LEWATI barang ke-index
    exact_knapsack(items, index + 1, remaining, chosen, solutions, max_sols)


def bounded_knapsack(items, index, remaining, chosen, best):
    """
    Mencari kombinasi barang dengan total MAKSIMUM tapi <= target.
    Hasil terbaik disimpan di best[0] (list bersifat mutable untuk pass by ref).

    Parameter:
      items     : list[int]  - daftar berat semua barang
      index     : int        - indeks barang yang sedang dipertimbangkan
      remaining : int        - sisa kapasitas yang tersedia
      chosen    : list[int]  - barang yang sudah dipilih saat ini
      best      : list[list] - best[0] = solusi terbaik sejauh ini
    """
    # Update solusi terbaik jika total saat ini lebih besar
    current_total = sum(chosen)
    if current_total > sum(best[0]):
        best[0] = chosen[:]

    # Basis: barang habis
    if index >= len(items):
        return

    # Pilihan 1: MASUKKAN barang ke-index (jika masih muat)
    if items[index] <= remaining:
        chosen.append(items[index])
        bounded_knapsack(items, index + 1, remaining - items[index], chosen, best)
        chosen.pop()    # backtrack

    # Pilihan 2: LEWATI barang ke-index
    bounded_knapsack(items, index + 1, remaining, chosen, best)


def run_knapsack():
    """Program utama Knapsack Problem."""
    print("=" * 50)
    print("          PROGRAM KNAPSACK PROBLEM")
    print("=" * 50)

    # Input daftar barang
    print("Masukkan berat barang (pisahkan dengan spasi).")
    print("Contoh default: 2 5 6 9 12 14 20")
    raw = input("Berat barang: ").strip()
    if not raw:
        items = [2, 5, 6, 9, 12, 14, 20]
        print(f"Menggunakan default: {items}")
    else:
        try:
            items = list(map(int, raw.split()))
            if any(w <= 0 for w in items):
                print("Semua berat harus > 0, menggunakan default.")
                items = [2, 5, 6, 9, 12, 14, 20]
        except ValueError:
            print("Input tidak valid, menggunakan default.")
            items = [2, 5, 6, 9, 12, 14, 20]

    # Input berat target
    while True:
        try:
            target = int(input("Masukkan berat target: "))
            if target > 0:
                break
            print("Target harus > 0!")
        except ValueError:
            print("Input tidak valid.")

    print(f"\nBarang   : {items}")
    print(f"Target   : {target}")
    print(f"Total barang: {len(items)}")
    print(f"\nMencari solusi...\n")

    # ---- Versi 1: Exact (tepat = target) ----
    solutions = []
    exact_knapsack(items, 0, target, [], solutions)

    if solutions:
        print(f"[Exact] Ditemukan {len(solutions)} kombinasi dengan total TEPAT {target}:")
        for i, sol in enumerate(solutions):
            print(f"  Solusi {i+1:>3}: {sol} → total = {sum(sol)}")
    else:
        print(f"[Exact] Tidak ada kombinasi yang totalnya tepat {target}.")

    # ---- Versi 2: Bounded (maksimum <= target) ----
    best = [[]]     # list agar bisa dimodifikasi dalam rekursi
    items_sorted = sorted(items)    # urutkan untuk pruning lebih baik
    bounded_knapsack(items_sorted, 0, target, [], best)

    print(f"\n[Bounded] Kombinasi terbaik (total maksimum ≤ {target}):")
    if best[0]:
        total = sum(best[0])
        sisa  = target - total
        print(f"  Barang dipilih : {best[0]}")
        print(f"  Total berat    : {total}")
        print(f"  Sisa kapasitas : {sisa}")
    else:
        print("  Tidak ada barang yang bisa dimasukkan.")

    print()


# ============================================================
# MENU UTAMA
# ============================================================

def main():
    """Menu utama untuk memilih program yang akan dijalankan."""
    print("\n" + "=" * 50)
    print("   TUGAS REKURSIF - ALGORITMA BACKTRACKING")
    print("=" * 50)

    while True:
        print("\nPilih program:")
        print("  1. N-Queens (N-Ratu)")
        print("  2. Knight's Tour (Tur Kuda)")
        print("  3. Knapsack Problem")
        print("  4. Jalankan Semua")
        print("  0. Keluar")

        pilihan = input("\nPilihan Anda: ").strip()

        if pilihan == "1":
            run_nqueens()
        elif pilihan == "2":
            run_knights_tour()
        elif pilihan == "3":
            run_knapsack()
        elif pilihan == "4":
            run_nqueens()
            run_knights_tour()
            run_knapsack()
        elif pilihan == "0":
            print("Program selesai. Terima kasih!")
            break
        else:
            print("Pilihan tidak valid. Masukkan 0-4.")


if __name__ == "__main__":
    main()
