import copy
# Cek value dari x dan y (horizontal dan vertikal) .

def is_valid(arr, x, y, num):
    arr[x][y] = num
        #melakukan pengecekan agar column y tidak double

    column_list = [arr[i][y] for i in range(9)] 
    zeroes = column_list.count(0) 
    if zeroes != 0: zeroes -= 1 # cek jika ada lebih dari 0 angka nol maka kurangi 1 karena himpunan array akan memiliki satu 0
    if len(set(column_list)) + zeroes != 9: 
        return False

     #melakukan pengecekan agar column y tidak double

    row_list = [arr[x][j] for j in range(9)]
    zeroes = row_list.count(0)
    if zeroes != 0: zeroes -= 1
    if len(set(row_list)) + zeroes != 9:  # cek jika ada lebih dari 0 angka nol maka kurangi 1 karena himpunan array akan memiliki satu 0
        return False

     # Cek jika ada yang double dalam box
    row_no = (x//3)*3 # angka pada box horizonal
    col_no = (y//3)*3 # angka pada box vertikal

   
    box_list = [arr[i][j] for i in range(row_no, row_no+3) for j in range(col_no, col_no+3)]
    zeroes = box_list.count(0)
    if zeroes != 0: zeroes -= 1
    if len(set(box_list)) + zeroes != 9:
        return False

    return True
     
# mengambil dari horizontal dan vertikal (x dan y) dan 
#mengembalikan koordinat 0 pertama yang ditemukannya
def empty_cell(arr):
    for x, i in enumerate(arr):
        for y, j in enumerate(i):
            if j == 0:
                return (x, y)
    return None

# Ini memecahkan papan sudoku menggunakan algoritma backtracking.
# Fungsi ini membutuhkan array Vertikal dan horizonal(x dan y) 9x9,
# lalu Mengembalikan 3 objek, satu adalah nilai boolean jika papan 
#terpecahkan atau tidak, yang kedua adalah langkah-langkah 2D (vertikal dan horizontal)
# array berisi koordinat x dan y papan yang diubah nilainya contohnya ([["3x3":3]])
# Ketiga adalah papan array terakhir. Penting untuk dikembalikan jika 
#papan kasus belum terselesaikan sepenuhnya itu menunjukkan sampai 
# dimana masalah itu diselesaikan. Berikut main function algoritma backtrackingnya
def solve(arr, steps):
   # Jika tidak ada sel kosong yang tersisa maka papan terpecahkan dan kembali
    cell = empty_cell(arr)
    if cell == None:
        return (True, steps, arr)

    x, y = cell
    for i in range(1, 10):
       # Memeriksa apakah penambahan nilai ini valid menurut aturan sudoku
        if is_valid(copy.deepcopy(arr), x, y, i):
            arr[x][y] = i
            steps.append([f"{x}x{y}",  i])
            a, steps, arr = solve(arr, steps)
            if a:
                return True, steps, arr
            
            arr[x][y] = 0
            steps.append([f"{x}x{y}",  " "])


    return False, steps, arr


