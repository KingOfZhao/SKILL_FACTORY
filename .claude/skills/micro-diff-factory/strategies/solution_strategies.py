"""
微分求解策略库

支持多种优化算法：
1. 模拟退火 (Simulated Annealing)
2. 粒子群优化 (Particle Swarm Optimization)
3. 梯度下降 (Gradient Descent)
4. 线性规划 (Linear Programming)
5. 遗传算法 (Genetic Algorithm)
6. 动态规划 (Dynamic Programming)
"""

import random
import math
from typing import Callable, List, Tuple, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class SolutionStrategyType(Enum):
    """求解策略类型"""
    SIMULATED_ANNEALING = "simulated_annealing"
    PARTICLE_SWARM = "particle_swarm"
    GRADIENT_DESCENT = "gradient_descent"
    LINEAR_PROGRAMMING = "linear_programming"
    GENETIC_ALGORITHM = "genetic_algorithm"
    DYNAMIC_PROGRAMMING = "dynamic_programming"


@dataclass
class SolutionState:
    """解的状态"""
    variables: Dict[str, float]
    objective_value: float
    iteration: int
    is_feasible: bool
    constraint_violations: List[str] = None

    def __post_init__(self):
        if self.constraint_violations is None:
            self.constraint_violations = []


@dataclass
class OptimizationConfig:
    """优化配置"""
    max_iterations: int = 1000
    convergence_threshold: float = 1e-6
    random_seed: Optional[int] = None
    verbose: bool = True


class SimulatedAnnealing:
    """
    模拟退火算法

    适用于：全局优化、离散问题、组合优化
    特点：避免局部最优，适合复杂非线性问题
    """

    def __init__(self,
                 initial_temperature: float = 1000.0,
                 cooling_rate: float = 0.95,
                 min_temperature: float = 1e-8):
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.min_temperature = min_temperature

    def solve(self,
              objective_function: Callable[[Dict[str, float]], float],
              initial_solution: Dict[str, float],
              bounds: Dict[str, Tuple[float, float]],
              constraints: Optional[Callable[[Dict[str, float]], bool]] = None,
              config: OptimizationConfig = None) -> SolutionState:
        """
        使用模拟退火算法求解优化问题

        Args:
            objective_function: 目标函数，接受变量字典，返回目标值
            initial_solution: 初始解
            bounds: 变量边界，{变量名: (最小值, 最大值)}
            constraints: 约束函数，返回是否满足约束
            config: 优化配置

        Returns:
            最优解状态
        """
        if config is None:
            config = OptimizationConfig()

        if config.random_seed is not None:
            random.seed(config.random_seed)

        current_solution = initial_solution.copy()
        current_value = objective_function(current_solution)
        best_solution = current_solution.copy()
        best_value = current_value

        temperature = self.initial_temperature
        iteration = 0

        while temperature > self.min_temperature and iteration < config.max_iterations:
            # 生成邻域解
            neighbor = self._generate_neighbor(current_solution, bounds)
            neighbor_value = objective_function(neighbor)

            # 检查约束
            if constraints and not constraints(neighbor):
                iteration += 1
                continue

            # 计算接受概率
            delta = neighbor_value - current_value

            if delta < 0 or random.random() < math.exp(-delta / temperature):
                current_solution = neighbor
                current_value = neighbor_value

                # 更新最优解
                if current_value < best_value:
                    best_solution = current_solution.copy()
                    best_value = current_value

                    if config.verbose and iteration % 100 == 0:
                        print(f"[模拟退火] 迭代 {iteration}: 最优值 = {best_value:.6f}, 温度 = {temperature:.2f}")

            # 降温
            temperature *= self.cooling_rate
            iteration += 1

            # 检查收敛
            if iteration > 10 and abs(current_value - best_value) < config.convergence_threshold:
                break

        return SolutionState(
            variables=best_solution,
            objective_value=best_value,
            iteration=iteration,
            is_feasible=True if constraints is None else constraints(best_solution)
        )

    def _generate_neighbor(self,
                          current_solution: Dict[str, float],
                          bounds: Dict[str, Tuple[float, float]],
                          step_size: float = 0.1) -> Dict[str, float]:
        """生成邻域解"""
        neighbor = current_solution.copy()

        for var_name in neighbor.keys():
            min_val, max_val = bounds[var_name]

            # 随机扰动
            delta = random.uniform(-step_size, step_size)
            neighbor[var_name] = max(min_val, min(max_val, neighbor[var_name] + delta))

        return neighbor


class ParticleSwarmOptimization:
    """
    粒子群优化算法

    适用于：连续优化、全局优化、函数优化
    特点：收敛速度快，适合高维问题
    """

    def __init__(self,
                 swarm_size: int = 30,
                 inertia_weight: float = 0.7,
                 cognitive_weight: float = 1.5,
                 social_weight: float = 1.5):
        self.swarm_size = swarm_size
        self.inertia_weight = inertia_weight
        self.cognitive_weight = cognitive_weight
        self.social_weight = social_weight

    def solve(self,
              objective_function: Callable[[Dict[str, float]], float],
              bounds: Dict[str, Tuple[float, float]],
              constraints: Optional[Callable[[Dict[str, float]], bool]] = None,
              config: OptimizationConfig = None) -> SolutionState:
        """
        使用粒子群优化算法求解优化问题

        Args:
            objective_function: 目标函数
            bounds: 变量边界
            constraints: 约束函数
            config: 优化配置

        Returns:
            最优解状态
        """
        if config is None:
            config = OptimizationConfig()

        if config.random_seed is not None:
            random.seed(config.random_seed)

        # 初始化粒子群
        particles, velocities = self._initialize_swarm(bounds)
        personal_best_positions = particles.copy()
        personal_best_values = [objective_function(p) for p in particles]

        # 全局最优
        global_best_idx = min(range(len(personal_best_values)),
                              key=lambda i: personal_best_values[i])
        global_best_position = personal_best_positions[global_best_idx].copy()
        global_best_value = personal_best_values[global_best_idx]

        iteration = 0
        while iteration < config.max_iterations:
            # 更新粒子
            for i in range(self.swarm_size):
                # 更新速度
                velocities[i] = self._update_velocity(
                    velocities[i],
                    particles[i],
                    personal_best_positions[i],
                    global_best_position,
                    bounds
                )

                # 更新位置
                particles[i] = self._update_position(
                    particles[i],
                    velocities[i],
                    bounds
                )

                # 检查约束
                if constraints and not constraints(particles[i]):
                    continue

                # 评估粒子
                current_value = objective_function(particles[i])

                # 更新个人最优
                if current_value < personal_best_values[i]:
                    personal_best_positions[i] = particles[i].copy()
                    personal_best_values[i] = current_value

                    # 更新全局最优
                    if current_value < global_best_value:
                        global_best_position = particles[i].copy()
                        global_best_value = current_value

                        if config.verbose and iteration % 100 == 0:
                            print(f"[粒子群] 迭代 {iteration}: 最优值 = {global_best_value:.6f}")

            iteration += 1

            # 检查收敛
            if iteration > 10 and self._check_convergence(particles, config.convergence_threshold):
                break

        return SolutionState(
            variables=global_best_position,
            objective_value=global_best_value,
            iteration=iteration,
            is_feasible=True if constraints is None else constraints(global_best_position)
        )

    def _initialize_swarm(self, bounds: Dict[str, Tuple[float, float]]) -> Tuple[List[Dict], List[Dict]]:
        """初始化粒子群和速度"""
        particles = []
        velocities = []

        for _ in range(self.swarm_size):
            particle = {}
            velocity = {}

            for var_name, (min_val, max_val) in bounds.items():
                particle[var_name] = random.uniform(min_val, max_val)
                velocity[var_name] = random.uniform(-1, 1) * (max_val - min_val) * 0.1

            particles.append(particle)
            velocities.append(velocity)

        return particles, velocities

    def _update_velocity(self,
                        velocity: Dict[str, float],
                        position: Dict[str, float],
                        personal_best: Dict[str, float],
                        global_best: Dict[str, float],
                        bounds: Dict[str, Tuple[float, float]]) -> Dict[str, float]:
        """更新粒子速度"""
        new_velocity = {}

        for var_name in position.keys():
            r1 = random.random()
            r2 = random.random()

            new_velocity[var_name] = (
                self.inertia_weight * velocity[var_name] +
                self.cognitive_weight * r1 * (personal_best[var_name] - position[var_name]) +
                self.social_weight * r2 * (global_best[var_name] - position[var_name])
            )

            # 限制速度
            max_val, min_val = bounds[var_name]
            max_velocity = (max_val - min_val) * 0.5
            new_velocity[var_name] = max(-max_velocity, min(max_velocity, new_velocity[var_name]))

        return new_velocity

    def _update_position(self,
                        position: Dict[str, float],
                        velocity: Dict[str, float],
                        bounds: Dict[str, Tuple[float, float]]) -> Dict[str, float]:
        """更新粒子位置"""
        new_position = {}

        for var_name, (min_val, max_val) in bounds.items():
            new_position[var_name] = max(min_val, min(max_val, position[var_name] + velocity[var_name]))

        return new_position

    def _check_convergence(self, particles: List[Dict], threshold: float) -> bool:
        """检查收敛性"""
        if len(particles) < 2:
            return False

        # 计算粒子之间的平均距离
        total_distance = 0
        count = 0

        for i in range(len(particles)):
            for j in range(i + 1, len(particles)):
                distance = self._calculate_distance(particles[i], particles[j])
                total_distance += distance
                count += 1

        avg_distance = total_distance / count if count > 0 else 0

        return avg_distance < threshold

    def _calculate_distance(self, p1: Dict, p2: Dict) -> float:
        """计算两个解之间的欧氏距离"""
        distance = 0.0
        for var_name in p1.keys():
            distance += (p1[var_name] - p2[var_name]) ** 2
        return math.sqrt(distance)


class GradientDescent:
    """
    梯度下降算法

    适用于：可微函数优化、凸优化
    特点：收敛速度快，但容易陷入局部最优
    """

    def __init__(self,
                 learning_rate: float = 0.01,
                 momentum: float = 0.9):
        self.learning_rate = learning_rate
        self.momentum = momentum

    def solve(self,
              objective_function: Callable[[Dict[str, float]], float],
              gradient_function: Callable[[Dict[str, float]], Dict[str, float]],
              initial_solution: Dict[str, float],
              bounds: Optional[Dict[str, Tuple[float, float]]] = None,
              config: OptimizationConfig = None) -> SolutionState:
        """
        使用梯度下降算法求解优化问题

        Args:
            objective_function: 目标函数
            gradient_function: 梯度函数
            initial_solution: 初始解
            bounds: 变量边界
            config: 优化配置

        Returns:
            最优解状态
        """
        if config is None:
            config = OptimizationConfig()

        current_solution = initial_solution.copy()
        current_value = objective_function(current_solution)

        best_solution = current_solution.copy()
        best_value = current_value

        velocity = {var: 0.0 for var in current_solution.keys()}
        iteration = 0

        while iteration < config.max_iterations:
            # 计算梯度
            gradient = gradient_function(current_solution)

            # 更新速度（带动量的梯度下降）
            for var_name in current_solution.keys():
                velocity[var_name] = (
                    self.momentum * velocity[var_name] -
                    self.learning_rate * gradient[var_name]
                )

                # 更新位置
                current_solution[var_name] += velocity[var_name]

                # 应用边界约束
                if bounds and var_name in bounds:
                    min_val, max_val = bounds[var_name]
                    current_solution[var_name] = max(min_val, min(max_val, current_solution[var_name]))

            # 计算新值
            current_value = objective_function(current_solution)

            # 更新最优解
            if current_value < best_value:
                best_solution = current_solution.copy()
                best_value = current_value

                if config.verbose and iteration % 100 == 0:
                    print(f"[梯度下降] 迭代 {iteration}: 最优值 = {best_value:.6f}")

            iteration += 1

            # 检查收敛
            if iteration > 10 and abs(current_value - best_value) < config.convergence_threshold:
                break

        return SolutionState(
            variables=best_solution,
            objective_value=best_value,
            iteration=iteration,
            is_feasible=True
        )


class OptimizationStrategySelector:
    """优化策略选择器"""

    @staticmethod
    def select_strategy(problem_type: str,
                       problem_complexity: str,
                       variable_count: int) -> SolutionStrategyType:
        """
        根据问题特征选择合适的优化策略

        Args:
            problem_type: 问题类型
            problem_complexity: 问题复杂度
            variable_count: 变量数量

        Returns:
            推荐的策略类型
        """
        # 高维问题 → 粒子群
        if variable_count > 20:
            return SolutionStrategyType.PARTICLE_SWARM

        # 复杂非线性问题 → 模拟退火
        if problem_complexity in ['complex', 'expert']:
            return SolutionStrategyType.SIMULATED_ANNEALING

        # 可微函数 → 梯度下降
        if problem_type in ['optimization', 'continuous']:
            return SolutionStrategyType.GRADIENT_DESCENT

        # 线性问题 → 线性规划
        if problem_type in ['linear', 'convex']:
            return SolutionStrategyType.LINEAR_PROGRAMMING

        # 默认 → 梯度下降
        return SolutionStrategyType.GRADIENT_DESCENT


# 示例使用
if __name__ == "__main__":
    # 示例 1: 模拟退火 - 优化蓝牙连接超时和重连间隔
    def bluetooth_objective(variables):
        """
        目标：最小化连接不稳定分数

        variables:
        - connection_timeout: 连接超时 (5-60 秒)
        - reconnect_delay: 重连延迟 (1-10 秒)
        - max_retries: 最大重试次数 (1-10)
        """
        timeout = variables['connection_timeout']
        delay = variables['reconnect_delay']
        retries = variables['max_retries']

        # 假设的目标函数：越大的超时和重连次数越稳定，但越大的延迟越差
        instability = (
            (1.0 / timeout) * 100 +  # 超时越大越好
            delay * 10 +  # 延迟越小越好
            (1.0 / retries) * 50  # 重试次数越多越好
        )

        return instability

    sa = SimulatedAnnealing(initial_temperature=1000, cooling_rate=0.95)
    result = sa.solve(
        objective_function=bluetooth_objective,
        initial_solution={'connection_timeout': 10, 'reconnect_delay': 2, 'max_retries': 3},
        bounds={
            'connection_timeout': (5, 60),
            'reconnect_delay': (1, 10),
            'max_retries': (1, 10)
        },
        config=OptimizationConfig(max_iterations=500, verbose=True)
    )

    print("\n模拟退火结果:")
    print(f"最优解: {result.variables}")
    print(f"最优值: {result.objective_value:.6f}")
    print(f"迭代次数: {result.iteration}")

    # 示例 2: 粒子群优化 - 优化图表渲染参数
    def chart_objective(variables):
        """
        目标：最小化渲染性能分数（分数越高越好，所以我们要最小化负分数）

        variables:
        - update_interval: 更新间隔 (100-2000 毫秒)
        - max_data_points: 最大数据点 (20-500)
        - cache_size: 缓存大小 (10-100 MB)
        """
        interval = variables['update_interval']
        max_points = variables['max_data_points']
        cache_size = variables['cache_size']

        # 性能分数：更新间隔越大越好，数据点越少越好，缓存越大越好
        # 我们最小化负分数
        performance = -(
            (interval / 2000) * 0.4 +
            (1 - max_points / 500) * 0.3 +
            (cache_size / 100) * 0.3
        )

        return performance

    pso = ParticleSwarmOptimization(swarm_size=30)
    result = pso.solve(
        objective_function=chart_objective,
        bounds={
            'update_interval': (100, 2000),
            'max_data_points': (20, 500),
            'cache_size': (10, 100)
        },
        config=OptimizationConfig(max_iterations=500, verbose=True)
    )

    print("\n粒子群优化结果:")
    print(f"最优解: {result.variables}")
    print(f"最优值: {result.objective_value:.6f}")
    print(f"迭代次数: {result.iteration}")
