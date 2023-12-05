from django.http import JsonResponse
from django.shortcuts import render
from .solver import empty_cell, solve
from .apps import boards
import random
import copy


# Halaman utama, memilih papan acak dari 'papan' dan juga melewati opsi kecepatan.
# Initial_board adalah keadaan awal papan dan merupakan variabel global
def home(response):
    global initial_board

    initial_board = random.choice(boards)
    
# Menyalin array sehingga initial_board tidak berubah
    # ketika perubahan dilakukan pada sudoku_board.

    sudoku_board = copy.deepcopy(initial_board)
    speed_options = {
                    "Normal": 0.3,
                    "Fast": 0.2,
                    "GodSpeed": 0,
                    }
    context = {
        "sudoku_board":sudoku_board,
        "speed_options":speed_options,
    }

    return render(response, 'main/index.html', context)

# Dipanggil melalui panggilan AJAX ketika pengguna mengubah nomor di papan.
# Ini mengembalikan respons JSON yang berisi nilai boolean jika benar
# menggunakan fungsi dari solver.py dan juga mengembalikan nilai boolean apakah semua sel terselesaikan.
def check(response):
    if response.method == "POST":
       
# Data berisi koordinat x dan y elemen dalam array yang diubah,
        # nilai yang diubah menjadi.
        data = response.POST
        sudoku_board = copy.deepcopy(initial_board)
        x, y = data.get('pos').split("x")
        x, y = int(x), int(y)
        val = data.get('val')

        # Mengembalikan False jika nilainya bukan digit atau 0 atau jika memiliki lebih dari satu karakter
       
        if not str(val).isdigit() or int(val) == 0 or len(str(val)) > 1:
            return JsonResponse({'is_correct': False, 'all_solved':False})

       
# Mengubah nilai tersebut di papan yang disalin dan meneruskannya ke fungsi penyelesaian dari solver.py
        sudoku_board[x][y] = int(val)
        
        is_correct, _, _ = solve(sudoku_board, [])

       # Melakukan perubahan pada board asli jika sudah benar
        if is_correct:
            initial_board[x][y] = int(val)
        else:
            initial_board[x][y] = 0

       
# Memeriksa apakah semua sel terpecahkan
        all_solved = not bool(empty_cell(initial_board))

        data = {
            'is_correct': is_correct,
            'all_solved':all_solved,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({})

# Mengembalikan respons JSON yang berisi langkah-langkah dan nilai boolean yang memberitahukan apakah masalah tersebut terselesaikan atau tidak
# Langkah adalah array 2D yang berisi koordinat x dan y, dan nilainya diubah
# Dipanggil dengan panggilan AJAX ketika pengguna mengklik selesaikan
def get_steps(response):
    if response.method == "POST":
        sudoku_board = copy.deepcopy(initial_board)  # Menyalin contoh papan awal saat ini
        d = []
        if_solved, steps, _ = solve(sudoku_board, d)
        return JsonResponse({"steps":steps, "if_solved":if_solved})
    else:
        return JsonResponse({})
