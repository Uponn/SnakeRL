from collections import defaultdict


class AStar:
    def __init__(self, snake, apple):
        self.snake = snake
        self.apple = apple

    def compute_h(self, xy):
        return abs(xy[0] - self.apple.x) + abs(xy[1] - self.apple.y)

    def reconstruct_path(self, came_from, current, start):
        total_path = [current]
        flag = False
        while not flag:
            current = came_from[current]
            total_path.insert(0, current)
            if current == start:
                flag = True
        return total_path

    def compute(self, start, end, coords_to_avoid):
        coords_to_avoid.remove(start)
        open_list = []
        closed_list = {}

        open_list.append(start)

        g_score = defaultdict(lambda: float('-inf'))
        g_score[start] = 0
        f_score = defaultdict(int)
        while open_list:
            current = min(open_list, key=f_score.get)
            if current == end:
                return self.reconstruct_path(closed_list, current, start)

            open_list.remove(current)

            for neighbors in [(10, 0), (-10, 0), (0, 10), (0, -10)]:
                neighbor = tuple(x + y for x, y in zip(current, neighbors))
                if neighbor in closed_list or neighbor in coords_to_avoid:
                    continue
                tentative_gscore = g_score[current] + 1
                if neighbor not in open_list:
                    open_list.append(neighbor)
                elif tentative_gscore >= g_score[neighbor]:
                    continue
                closed_list[neighbor] = current
                g_score[neighbor] = tentative_gscore
                f_score[neighbor] = tentative_gscore + self.compute_h(neighbor)
