from functools import lru_cache

import numpy as np
from scipy.signal import convolve2d
from numba import njit


class GameOfLife:
    regions_map = {}

    def __init__(self, width, height):
        self.grid = np.zeros((height, width), dtype=int)
        self.width = width
        self.height = height

    def fill_random(self, seed=None):
        if seed is not None:
            np.random.seed(seed)
        self.grid = np.random.randint(0, 2, size=(self.height, self.width))

    @staticmethod
    @njit()
    def __split_region(matrix):
        """Функция для разделения матрицы на 4 равные части
        с расширением границы на 1 клетку во все стороны

        Параметры:
        matrix (ndarray): исходная матрица

        Возвращает:
        part1, part2, part3, part4 (ndarrays): четыре части матрицы"""
        rows, cols = matrix.shape
        mid_row, mid_col = rows // 2, cols // 2

        part1 = matrix[:mid_row + 1, :mid_col + 1]
        part2 = matrix[:mid_row + 1, mid_col - 1:]
        part3 = matrix[mid_row - 1:, :mid_col + 1]
        part4 = matrix[mid_row - 1:, mid_col - 1:]

        return part1, part2, part3, part4

    @staticmethod
    @njit()
    def __merge_region(part1, part2, part3, part4):
        """
        Функция для объединения 4 частей матрицы в одну целую матрицу

        Параметры:
        part1, part2, part3, part4 (ndarrays): четыре части матрицы

        Возвращает:
        merged_matrix (ndarray): объединенная матрица
        """

        height = part1.shape[0] + part3.shape[0]
        width = part1.shape[1] + part2.shape[1]
        merged_matrix = np.zeros((height, width), dtype=part1.dtype)

        merged_matrix[:part1.shape[0], :part1.shape[1]] = part1
        merged_matrix[:part2.shape[0], part2.shape[1]:] = part2
        merged_matrix[part3.shape[0]:, :part3.shape[1]] = part3
        merged_matrix[part4.shape[0]:, part4.shape[1]:] = part4

        return merged_matrix

    def update_region(self, region: np.ndarray):
        """
        Обновляет область (region) в соответствии с правилами игры.

        Если область уже была рассмотрена ранее, то возвращает ее кэшированное значение.
        В противном случае разбивает область на меньшие части, рекурсивно обновляет их,
        а затем объединяет обратно в одну область.

        Args:
            region (np.ndarray): Область, которую нужно обновить.

        Returns:
            np.ndarray: Обновленная область.
        """

        region_bytes = region.tobytes()
        next_step_region = self.regions_map.get(region_bytes)

        if next_step_region is not None:
            return next_step_region

        rows, cols = region.shape
        if rows == 4 or cols == 4:
            result = self.__get_next_region(region)[1:-1, 1:-1]
        else:
            region_parts = self.__split_region(region)
            updated_regions = [
                self.update_region(region_part)
                for region_part in region_parts
            ]
            result = self.__merge_region(*updated_regions)

        self.regions_map[region_bytes] = result
        return result

    def update(self):
        new_grid = np.copy(self.grid)
        extended_region = np.pad(new_grid, pad_width=1, mode='wrap')
        new_grid = self.update_region(extended_region)
        self.grid = new_grid

    def update_lazy(self):
        new_grid = np.zeros_like(self.grid)
        neighbors = self.get_neighbors(self.grid)
        birth = (neighbors == 3) & (self.grid == 0)
        survive = ((neighbors == 2) | (neighbors == 3)) & (self.grid == 1)
        new_grid[birth] = 1
        new_grid[survive] = 1

        self.grid = new_grid

    def __get_next_region(self, region):
        new_region = np.zeros_like(region)
        neighbors = self.get_neighbors(region)
        birth = (neighbors == 3) & (region == 0)
        survive = ((neighbors == 2) | (neighbors == 3)) & (region == 1)
        new_region[birth] = 1
        new_region[survive] = 1

        return new_region

    def get_neighbors(self, region):
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])
        neighbors = convolve2d(region, kernel, mode='same', boundary='wrap')
        return neighbors
