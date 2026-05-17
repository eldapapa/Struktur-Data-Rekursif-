# Tugas Rekursif — Algoritma Backtracking

Program Python yang mengimplementasikan tiga algoritma backtracking rekursif klasik dalam satu file interaktif.

---

## Daftar Isi

- [Deskripsi Program](#deskripsi-program)
- [Cara Menjalankan](#cara-menjalankan)
- [Soal 1: N-Queens](#soal-1-n-queens-n-ratu)
- [Soal 2: Knight's Tour](#soal-2-knights-tour-tur-kuda)
- [Soal 3: Knapsack Problem](#soal-3-knapsack-problem)
- [Struktur Kode](#struktur-kode)
- [Contoh Output](#contoh-output)

---

## Deskripsi Program

| # | Masalah | Algoritma | Input Pengguna |
|---|---------|-----------|----------------|
| 1 | N-Queens | Backtracking rekursif | Ukuran papan N |
| 2 | Knight's Tour | Backtracking + Warnsdorff | Ukuran papan, posisi awal |
| 3 | Knapsack | Backtracking rekursif (pohon biner) | Daftar berat, berat target |

---

## Cara Menjalankan

**Prasyarat:** Python 3.x (tidak ada library tambahan yang dibutuhkan)

```bash
python tugas_rekursif.py
```

Setelah dijalankan, pilih program dari menu:

```
==================================================
   TUGAS REKURSIF - ALGORITMA BACKTRACKING
==================================================

Pilih program:
  1. N-Queens (N-Ratu)
  2. Knight's Tour (Tur Kuda)
  3. Knapsack Problem
  4. Jalankan Semua
  0. Keluar
```

---

## Soal 1: N-Queens (N-Ratu)

### Deskripsi

Tempatkan **N ratu** di papan catur **N×N** sehingga tidak ada dua ratu yang saling menyerang — tidak boleh berada di baris, kolom, atau diagonal yang sama.

### Pendekatan

Backtracking rekursif baris per baris:

```
Baris 0 → coba kolom 0..N-1
  └─ jika aman → Baris 1 → coba kolom 0..N-1
       └─ jika aman → Baris 2 → ...
            └─ Baris N → SOLUSI DITEMUKAN ✓
       └─ jika tidak aman → backtrack ke baris sebelumnya
```

### Fungsi-Fungsi

| Fungsi | Tugas |
|--------|-------|
| `is_safe_queen(board, row, col, n)` | Cek apakah posisi (row, col) aman dari serangan ratu lain |
| `solve_nqueens(board, row, n, solutions)` | Rekursi utama; menyimpan semua solusi ke list `solutions` |
| `print_nqueens_board(solution, n)` | Cetak papan dalam format visual |
| `run_nqueens()` | Fungsi driver: input, proses, output |

### Penjelasan `is_safe_queen`

```python
for r in range(row):
    c = board[r]
    if c == col:                        # kolom sama
        return False
    if abs(c - col) == abs(r - row):    # sediagonal
        return False
return True
```

Hanya perlu mengecek baris **di atas** posisi saat ini karena ratu diletakkan baris per baris dari atas ke bawah.

### Kompleksitas

| | Nilai |
|-|-------|
| Waktu (terburuk) | O(N!) |
| Ruang | O(N) untuk board, O(S×N) untuk S solusi |

---

## Soal 2: Knight's Tour (Tur Kuda)

### Deskripsi

Kuda catur harus mengunjungi **setiap petak** di papan N×N **tepat satu kali**, dimulai dari posisi yang ditentukan pengguna.

### 8 Langkah Legal Kuda

```
. X . X .
X . . . X
. . ♞ . .
X . . . X
. X . X .
```

Dalam kode direpresentasikan sebagai:
```python
KNIGHT_MOVES = [
    (-2, -1), (-2, +1),
    (-1, -2), (-1, +2),
    (+1, -2), (+1, +2),
    (+2, -1), (+2, +1)
]
```

### Pendekatan: Backtracking + Warnsdorff's Heuristic

**Heuristik Warnsdorff:** Di setiap langkah, pilih petak berikutnya yang memiliki **jumlah langkah lanjutan paling sedikit** (degree terkecil). Ini mencegah jalan buntu dan membuat solusi ditemukan hampir tanpa backtracking.

```python
next_moves.sort(key=lambda pos: get_degree(board, pos[0], pos[1], n))
```

### Fungsi-Fungsi

| Fungsi | Tugas |
|--------|-------|
| `get_valid_moves(board, row, col, n)` | Kembalikan daftar langkah valid dari posisi (row, col) |
| `get_degree(board, row, col, n)` | Hitung jumlah langkah lanjutan (untuk heuristik Warnsdorff) |
| `solve_knights_tour(board, row, col, move_num, n, path)` | Rekursi utama dengan backtracking |
| `print_knights_board(board, n)` | Cetak papan dengan nomor urut kunjungan |
| `print_knights_path(path, n)` | Cetak daftar langkah dalam format teks |
| `run_knights_tour()` | Fungsi driver: input, proses, output |

### Alur Rekursi

```
solve(r, c, move=1)
  ├─ Ambil semua langkah valid dari (r, c)
  ├─ Urutkan berdasar degree terkecil (Warnsdorff)
  └─ Untuk setiap (nr, nc):
       ├─ board[nr][nc] = move_num  → tandai dikunjungi
       ├─ rekursi(nr, nc, move+1)
       │    └─ jika True → SELESAI ✓
       └─ board[nr][nc] = -1       → backtrack
```

### Kompleksitas

| | Nilai |
|-|-------|
| Waktu (tanpa heuristik) | O(8^(N²)) dalam kasus terburuk |
| Waktu (dengan Warnsdorff) | Hampir linear dalam praktik |
| Ruang | O(N²) untuk board |

---

## Soal 3: Knapsack Problem

### Deskripsi

Diberikan daftar barang dengan berat masing-masing dan sebuah **berat target**. Cari kombinasi barang yang totalnya tepat sama dengan (atau tidak melebihi) target.

Contoh dari soal:
- Barang: `[2, 5, 6, 9, 12, 14, 20]`
- Target: `30`
- Salah satu solusi: `[2, 5, 9, 14]` → total = 30 ✓

### Pendekatan: Pohon Rekursi Biner

Setiap barang punya **dua pilihan**:

```
                  knapsack(0, sisa=30)
                 /                    \
     MASUKKAN item[0]=2            LEWATI item[0]
     knapsack(1, sisa=28)          knapsack(1, sisa=30)
        /         \                   /         \
  MASUKKAN      LEWATI          MASUKKAN      LEWATI
  item[1]=5    item[1]          item[1]=5    item[1]
      ...          ...              ...          ...
```

### Dua Versi Algoritma

**Versi 1 — `exact_knapsack`:** Mencari kombinasi yang totalnya **tepat = target**

```python
def exact_knapsack(items, index, remaining, chosen, solutions):
    if remaining == 0:          # SOLUSI TEPAT ditemukan
        solutions.append(chosen[:])
        return
    if index >= len(items) or remaining < 0:  # gagal, backtrack
        return
    # Pilih barang ini
    chosen.append(items[index])
    exact_knapsack(items, index + 1, remaining - items[index], chosen, solutions)
    chosen.pop()                # backtrack
    # Lewati barang ini
    exact_knapsack(items, index + 1, remaining, chosen, solutions)
```

**Versi 2 — `bounded_knapsack`:** Mencari kombinasi dengan total **maksimum ≤ target** (solusi terbaik)

### Fungsi-Fungsi

| Fungsi | Tugas |
|--------|-------|
| `exact_knapsack(items, index, remaining, chosen, solutions)` | Cari semua kombinasi tepat = target |
| `bounded_knapsack(items, index, remaining, chosen, best)` | Cari kombinasi maksimum ≤ target |
| `run_knapsack()` | Fungsi driver: input, proses, output |

### Kompleksitas

| | Nilai |
|-|-------|
| Waktu (terburuk) | O(2^N) |
| Ruang | O(N) untuk call stack rekursi |

> **Catatan:** Untuk N yang sangat besar (ribuan barang), solusi rekursif murni bisa lambat. Alternatifnya adalah Dynamic Programming yang memiliki kompleksitas O(N × W) di mana W adalah berat target.

---

## Struktur Kode

```
tugas_rekursif.py
│
├── # SOAL 1: N-QUEENS
│   ├── is_safe_queen()
│   ├── solve_nqueens()
│   ├── print_nqueens_board()
│   └── run_nqueens()
│
├── # SOAL 2: KNIGHT'S TOUR
│   ├── KNIGHT_MOVES  (konstanta 8 arah)
│   ├── get_valid_moves()
│   ├── get_degree()
│   ├── solve_knights_tour()
│   ├── print_knights_board()
│   ├── print_knights_path()
│   └── run_knights_tour()
│
├── # SOAL 3: KNAPSACK
│   ├── exact_knapsack()
│   ├── bounded_knapsack()
│   └── run_knapsack()
│
└── main()   ← menu utama
```

---

## Contoh Output

### N-Queens (N=6)

```
Ditemukan 4 solusi untuk N=6.

--- Solusi 1 ---
+---+---+---+---+---+---+
| . | Q | . | . | . | . |
+---+---+---+---+---+---+
| . | . | . | Q | . | . |
+---+---+---+---+---+---+
| . | . | . | . | . | Q |
+---+---+---+---+---+---+
| Q | . | . | . | . | . |
+---+---+---+---+---+---+
| . | . | Q | . | . | . |
+---+---+---+---+---+---+
| . | . | . | . | Q | . |
+---+---+---+---+---+---+
```

### Knight's Tour (6×6, mulai dari (1,1))

```
✓ SOLUSI DITEMUKAN! Kuda mengunjungi 36 petak.

+----+----+----+----+----+----+
|  1 | 28 |  9 | 20 |  3 | 30 |
+----+----+----+----+----+----+
| 10 | 21 |  2 | 29 | 16 | 19 |
+----+----+----+----+----+----+
| 35 |  8 | 27 | 18 | 31 |  4 |
+----+----+----+----+----+----+
| 22 | 11 | 34 | 15 | 26 | 17 |
+----+----+----+----+----+----+
|  7 | 36 | 13 | 24 |  5 | 32 |
+----+----+----+----+----+----+
| 12 | 23 |  6 | 33 | 14 | 25 |
+----+----+----+----+----+----+
```

### Knapsack (items=[2,5,6,9,12,14,20], target=30)

```
[Exact] Ditemukan 1 kombinasi dengan total TEPAT 30:
  Solusi   1: [2, 5, 9, 14] → total = 30

[Bounded] Kombinasi terbaik (total maksimum ≤ 30):
  Barang dipilih : [2, 5, 9, 14]
  Total berat    : 30
  Sisa kapasitas : 0
```

---

## Referensi Konsep

- **Backtracking:** Teknik pencarian solusi dengan mencoba semua kemungkinan secara rekursif dan membatalkan pilihan yang terbukti tidak mengarah ke solusi.
- **Warnsdorff's Rule:** Heuristik untuk Knight's Tour yang memprioritaskan petak dengan paling sedikit langkah lanjutan, ditemukan oleh H.C. von Warnsdorff (1823).
- **Knapsack Problem:** Masalah optimasi kombinatorial klasik yang termasuk kategori NP-Complete untuk versi keputusan umum.
