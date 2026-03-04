"""
微分可视化工具

提供可视化功能：
1. 变量关系图 (Variable Relationship Graph)
2. 优化轨迹图 (Optimization Trajectory Graph)
3. 约束可视化 (Constraint Visualization)
4. 敏感性分析图 (Sensitivity Analysis Graph)
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum


class GraphType(Enum):
    """图类型"""
    VARIABLE_RELATIONSHIP = "variable_relationship"
    OPTIMIZATION_TRAJECTORY = "optimization_trajectory"
    CONSTRAINT_VISUALIZATION = "constraint_visualization"
    SENSITIVITY_ANALYSIS = "sensitivity_analysis"


class EdgeType(Enum):
    """边类型"""
    DEPENDENCY = "dependency"
    CORRELATION = "correlation"
    CONSTRAINT = "constraint"
    INFLUENCE = "influence"


@dataclass
class VariableNode:
    """变量节点"""
    name: str
    value: float
    min_value: float
    max_value: float
    node_type: str  # input, output, intermediate
    description: str = ""


@dataclass
class VariableEdge:
    """变量边"""
    source: str
    target: str
    edge_type: EdgeType
    weight: float
    description: str = ""


@dataclass
class OptimizationPoint:
    """优化轨迹点"""
    iteration: int
    variables: Dict[str, float]
    objective_value: float
    is_feasible: bool


class VariableRelationshipGraph:
    """变量关系图生成器"""

    def __init__(self, title: str = "变量关系图"):
        self.title = title
        self.graph = nx.DiGraph()
        self.nodes: Dict[str, VariableNode] = {}
        self.edges: List[VariableEdge] = []

    def add_variable(self, variable: VariableNode):
        """添加变量节点"""
        self.nodes[variable.name] = variable
        self.graph.add_node(
            variable.name,
            value=variable.value,
            node_type=variable.node_type,
            description=variable.description
        )

    def add_relationship(self, edge: VariableEdge):
        """添加变量关系"""
        self.edges.append(edge)
        self.graph.add_edge(
            edge.source,
            edge.target,
            edge_type=edge.edge_type.value,
            weight=edge.weight,
            description=edge.description
        )

    def generate(self, output_path: Optional[str] = None, show: bool = True) -> str:
        """
        生成变量关系图

        Args:
            output_path: 输出文件路径
            show: 是否显示图形

        Returns:
            图形文件路径
        """
        if not output_path:
            output_path = f"{self.title.replace(' ', '_')}.png"

        # 创建图形
        plt.figure(figsize=(14, 10))

        # 设置布局
        pos = nx.spring_layout(self.graph, k=2, iterations=50)

        # 绘制节点
        input_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('node_type') == 'input']
        output_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('node_type') == 'output']
        intermediate_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('node_type') == 'intermediate']

        # 绘制不同类型的节点
        if input_nodes:
            nx.draw_networkx_nodes(
                self.graph, pos,
                nodelist=input_nodes,
                node_color='lightgreen',
                node_size=800,
                alpha=0.8,
                label='输入变量'
            )

        if output_nodes:
            nx.draw_networkx_nodes(
                self.graph, pos,
                nodelist=output_nodes,
                node_color='lightcoral',
                node_size=800,
                alpha=0.8,
                label='输出变量'
            )

        if intermediate_nodes:
            nx.draw_networkx_nodes(
                self.graph, pos,
                nodelist=intermediate_nodes,
                node_color='lightblue',
                node_size=600,
                alpha=0.8,
                label='中间变量'
            )

        # 绘制边
        dependency_edges = [
            (u, v) for u, v, d in self.graph.edges(data=True)
            if d.get('edge_type') == 'dependency'
        ]
        correlation_edges = [
            (u, v) for u, v, d in self.graph.edges(data=True)
            if d.get('edge_type') == 'correlation'
        ]
        constraint_edges = [
            (u, v) for u, v, d in self.graph.edges(data=True)
            if d.get('edge_type') == 'constraint'
        ]

        nx.draw_networkx_edges(
            self.graph, pos,
            edgelist=dependency_edges,
            edge_color='black',
            width=2,
            alpha=0.6,
            arrows=True,
            arrowsize=20,
            label='依赖关系'
        )

        nx.draw_networkx_edges(
            self.graph, pos,
            edgelist=correlation_edges,
            edge_color='purple',
            width=2,
            alpha=0.6,
            style='dashed',
            label='相关性'
        )

        nx.draw_networkx_edges(
            self.graph, pos,
            edgelist=constraint_edges,
            edge_color='red',
            width=2,
            alpha=0.6,
            style='dotted',
            label='约束关系'
        )

        # 绘制标签
        labels = {n: f"{n}\n{self.nodes[n].value:.2f}" for n in self.graph.nodes()}
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=8, font_weight='bold')

        # 添加标题和图例
        plt.title(self.title, fontsize=16, fontweight='bold', pad=20)
        plt.legend(loc='upper right')

        # 添加边权重标签
        edge_labels = {
            (u, v): f"{d['weight']:.2f}"
            for u, v, d in self.graph.edges(data=True)
        }
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels, font_size=7)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')

        if show:
            plt.show()
        else:
            plt.close()

        return output_path


class OptimizationTrajectoryGraph:
    """优化轨迹图生成器"""

    def __init__(self, title: str = "优化轨迹图"):
        self.title = title
        self.trajectory_points: List[OptimizationPoint] = []

    def add_point(self, point: OptimizationPoint):
        """添加轨迹点"""
        self.trajectory_points.append(point)

    def generate(self,
                output_path: Optional[str] = None,
                show: bool = True,
                variables_to_plot: Optional[List[str]] = None) -> str:
        """
        生成优化轨迹图

        Args:
            output_path: 输出文件路径
            show: 是否显示图形
            variables_to_plot: 要绘制的变量列表

        Returns:
            图形文件路径
        """
        if not output_path:
            output_path = f"{self.title.replace(' ', '_')}.png"

        if not self.trajectory_points:
            raise ValueError("没有轨迹点可以绘制")

        # 获取所有变量名
        all_variables = set()
        for point in self.trajectory_points:
            all_variables.update(point.variables.keys())

        # 如果没有指定变量，绘制前 4 个
        if variables_to_plot is None:
            variables_to_plot = list(all_variables)[:4]

        # 确定子图数量
        num_vars = len(variables_to_plot)

        # 创建图形
        fig, axes = plt.subplots(num_vars + 1, 1, figsize=(12, 4 * (num_vars + 1)))

        if num_vars == 1:
            axes = [axes[0], axes[1]]
        else:
            axes = list(axes)

        # 绘制每个变量的轨迹
        for i, var_name in enumerate(variables_to_plot):
            ax = axes[i]

            iterations = [point.iteration for point in self.trajectory_points]
            values = [point.variables.get(var_name, 0) for point in self.trajectory_points]

            # 绘制轨迹
            ax.plot(iterations, values, 'b-', linewidth=2, marker='o', markersize=4, label=var_name)

            # 标记不可行点
            infeasible_indices = [
                i for i, point in enumerate(self.trajectory_points)
                if not point.is_feasible
            ]
            if infeasible_indices:
                infeasible_iterations = [iterations[i] for i in infeasible_indices]
                infeasible_values = [values[i] for i in infeasible_indices]
                ax.scatter(infeasible_iterations, infeasible_values, c='red', s=100, marker='x', label='不可行')

            ax.set_xlabel('迭代次数', fontsize=10)
            ax.set_ylabel(var_name, fontsize=10)
            ax.set_title(f'{var_name} 的变化轨迹', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend()

        # 绘制目标函数值
        ax = axes[num_vars]
        iterations = [point.iteration for point in self.trajectory_points]
        objective_values = [point.objective_value for point in self.trajectory_points]

        ax.plot(iterations, objective_values, 'g-', linewidth=2, marker='o', markersize=4, label='目标函数值')

        # 标记不可行点
        infeasible_indices = [
            i for i, point in enumerate(self.trajectory_points)
            if not point.is_feasible
        ]
        if infeasible_indices:
            infeasible_iterations = [iterations[i] for i in infeasible_indices]
            infeasible_values = [objective_values[i] for i in infeasible_indices]
            ax.scatter(infeasible_iterations, infeasible_values, c='red', s=100, marker='x', label='不可行')

        ax.set_xlabel('迭代次数', fontsize=10)
        ax.set_ylabel('目标函数值', fontsize=10)
        ax.set_title('目标函数值的收敛轨迹', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()

        plt.suptitle(self.title, fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')

        if show:
            plt.show()
        else:
            plt.close()

        return output_path

    def generate_2d_trajectory(self,
                               var_x: str,
                               var_y: str,
                               output_path: Optional[str] = None,
                               show: bool = True) -> str:
        """
        生成二维优化轨迹图

        Args:
            var_x: x 轴变量名
            var_y: y 轴变量名
            output_path: 输出文件路径
            show: 是否显示图形

        Returns:
            图形文件路径
        """
        if not output_path:
            output_path = f"{self.title.replace(' ', '_')}_2d.png"

        # 提取 x 和 y 的值
        x_values = [point.variables.get(var_x, 0) for point in self.trajectory_points]
        y_values = [point.variables.get(var_y, 0) for point in self.trajectory_points]

        # 创建图形
        plt.figure(figsize=(10, 10))

        # 绘制轨迹线
        plt.plot(x_values, y_values, 'b-', linewidth=2, alpha=0.6, label='优化轨迹')

        # 绘制轨迹点（起点和终点特殊标记）
        plt.scatter(x_values[0], y_values[0], c='green', s=200, marker='o', label='起点', zorder=5)
        plt.scatter(x_values[-1], y_values[-1], c='red', s=200, marker='*', label='终点（最优解）', zorder=5)
        plt.scatter(x_values[1:-1], y_values[1:-1], c='blue', s=50, alpha=0.6, zorder=3)

        # 标记不可行点
        infeasible_indices = [
            i for i, point in enumerate(self.trajectory_points)
            if not point.is_feasible
        ]
        if infeasible_indices:
            infeasible_x = [x_values[i] for i in infeasible_indices]
            infeasible_y = [y_values[i] for i in infeasible_indices]
            plt.scatter(infeasible_x, infeasible_y, c='orange', s=100, marker='x', label='不可行点', zorder=4)

        # 添加迭代序号标签
        for i, (x, y) in enumerate(zip(x_values, y_values)):
            if i % max(1, len(x_values) // 10) == 0:  # 每隔 10% 的点标记一次
                plt.annotate(f'{i}', (x, y), fontsize=8, ha='center', va='bottom')

        plt.xlabel(var_x, fontsize=12)
        plt.ylabel(var_y, fontsize=12)
        plt.title(f'{self.title} - {var_x} vs {var_y}', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')

        if show:
            plt.show()
        else:
            plt.close()

        return output_path


class ConstraintVisualization:
    """约束可视化工具"""

    def visualize_1d_constraint(self,
                               variable_name: str,
                               constraint_func: callable,
                               bounds: Tuple[float, float],
                               output_path: Optional[str] = None,
                               show: bool = True) -> str:
        """
        可视化一维约束

        Args:
            variable_name: 变量名
            constraint_func: 约束函数，返回 True/False
            bounds: 变量边界
            output_path: 输出文件路径
            show: 是否显示图形

        Returns:
            图形文件路径
        """
        if not output_path:
            output_path = f"{variable_name}_constraint_1d.png"

        # 生成采样点
        x = np.linspace(bounds[0], bounds[1], 1000)
        feasible = [constraint_func(val) for val in x]

        # 创建图形
        plt.figure(figsize=(12, 4))

        # 绘制可行域和不可行域
        for i in range(len(x) - 1):
            if feasible[i]:
                plt.fill_between([x[i], x[i+1]], 0, 1, color='green', alpha=0.3)
            else:
                plt.fill_between([x[i], x[i+1]], 0, 1, color='red', alpha=0.3)

        # 绘制边界线
        boundary_points = []
        for i in range(len(feasible) - 1):
            if feasible[i] != feasible[i+1]:
                boundary_points.append(x[i])
                plt.axvline(x[i], color='blue', linestyle='--', linewidth=2)

        # 添加标签
        plt.xlabel(variable_name, fontsize=12)
        plt.yticks([])
        plt.title(f'{variable_name} 的约束可视化', fontsize=14, fontweight='bold')
        plt.legend(['约束边界'], loc='upper right')

        # 添加说明
        textstr = '绿色区域：可行域\n红色区域：不可行域\n蓝色虚线：约束边界'
        plt.text(0.02, 0.95, textstr, transform=plt.gca().transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')

        if show:
            plt.show()
        else:
            plt.close()

        return output_path

    def visualize_2d_constraint(self,
                                var_x_name: str,
                                var_y_name: str,
                                constraint_func: callable,
                                x_bounds: Tuple[float, float],
                                y_bounds: Tuple[float, float],
                                output_path: Optional[str] = None,
                                show: bool = True) -> str:
        """
        可视化二维约束

        Args:
            var_x_name: x 轴变量名
            var_y_name: y 轴变量名
            constraint_func: 约束函数
            x_bounds: x 变量边界
            y_bounds: y 变量边界
            output_path: 输出文件路径
            show: 是否显示图形

        Returns:
            图形文件路径
        """
        if not output_path:
            output_path = f"{var_x_name}_{var_y_name}_constraint_2d.png"

        # 生成网格
        x = np.linspace(x_bounds[0], x_bounds[1], 200)
        y = np.linspace(y_bounds[0], y_bounds[1], 200)
        X, Y = np.meshgrid(x, y)

        # 评估约束
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = 1 if constraint_func(X[i, j], Y[i, j]) else 0

        # 创建图形
        plt.figure(figsize=(10, 10))

        # 绘制等高图
        plt.contourf(X, Y, Z, levels=[0, 0.5, 1], colors=['red', 'green'], alpha=0.3)
        plt.contour(X, Y, Z, levels=[0.5], colors=['blue'], linewidths=2)

        plt.xlabel(var_x_name, fontsize=12)
        plt.ylabel(var_y_name, fontsize=12)
        plt.title(f'{var_x_name} vs {var_y_name} 的约束可视化', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)

        # 添加说明
        textstr = '绿色区域：可行域\n红色区域：不可行域\n蓝色线：约束边界'
        plt.text(0.02, 0.98, textstr, transform=plt.gca().transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')

        if show:
            plt.show()
        else:
            plt.close()

        return output_path


class SensitivityAnalysisGraph:
    """敏感性分析图生成器"""

    def __init__(self, title: str = "敏感性分析"):
        self.title = title
        self.sensitivity_data: Dict[str, List[Tuple[float, float]]] = {}

    def add_variable_sensitivity(self,
                                  variable_name: str,
                                  perturbations: List[float],
                                  objective_changes: List[float]):
        """
        添加变量的敏感性数据

        Args:
            variable_name: 变量名
            perturbations: 扰动值列表
            objective_changes: 对应的目标函数变化
        """
        self.sensitivity_data[variable_name] = list(zip(perturbations, objective_changes))

    def generate(self,
                output_path: Optional[str] = None,
                show: bool = True) -> str:
        """
        生成敏感性分析图

        Args:
            output_path: 输出文件路径
            show: 是否显示图形

        Returns:
            图形文件路径
        """
        if not output_path:
            output_path = f"{self.title.replace(' ', '_')}.png"

        if not self.sensitivity_data:
            raise ValueError("没有敏感性数据可以绘制")

        # 创建图形
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        # 1. 绘制敏感性曲线
        ax1 = axes[0]

        colors = plt.cm.rainbow(np.linspace(0, 1, len(self.sensitivity_data)))

        for (var_name, data), color in zip(self.sensitivity_data.items(), colors):
            perturbations = [p for p, _ in data]
            changes = [c for _, c in data]

            ax1.plot(perturbations, changes, marker='o', linewidth=2, label=var_name, color=color)

        ax1.set_xlabel('变量扰动', fontsize=12)
        ax1.set_ylabel('目标函数变化', fontsize=12)
        ax1.set_title('各变量的敏感性曲线', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # 2. 绘制敏感性条形图
        ax2 = axes[1]

        # 计算每个变量的平均敏感性
        sensitivities = {}
        for var_name, data in self.sensitivity_data.items():
            avg_sensitivity = np.mean([abs(c) for _, c in data])
            sensitivities[var_name] = avg_sensitivity

        # 排序
        sorted_vars = sorted(sensitivities.items(), key=lambda x: x[1], reverse=True)

        var_names = [item[0] for item in sorted_vars]
        var_sensitivities = [item[1] for item in sorted_vars]

        ax2.barh(var_names, var_sensitivities, color=colors[:len(var_names)])
        ax2.set_xlabel('平均敏感性（绝对值）', fontsize=12)
        ax2.set_title('各变量的敏感性排序', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')

        plt.suptitle(self.title, fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')

        if show:
            plt.show()
        else:
            plt.close()

        return output_path


# 示例使用
if __name__ == "__main__":
    # 示例 1: 变量关系图
    vrg = VariableRelationshipGraph("蓝牙连接稳定性优化 - 变量关系图")

    # 添加变量
    vrg.add_variable(VariableNode(
        name="connection_timeout",
        value=15.0,
        min_value=5.0,
        max_value=60.0,
        node_type="input",
        description="连接超时时间（秒）"
    ))

    vrg.add_variable(VariableNode(
        name="reconnect_delay",
        value=3.0,
        min_value=1.0,
        max_value=10.0,
        node_type="input",
        description="重连延迟（秒）"
    ))

    vrg.add_variable(VariableNode(
        name="stability_score",
        value=0.75,
        min_value=0.0,
        max_value=1.0,
        node_type="output",
        description="连接稳定性分数"
    ))

    vrg.add_variable(VariableNode(
        name="connection_success_rate",
        value=0.85,
        min_value=0.0,
        max_value=1.0,
        node_type="intermediate",
        description="连接成功率"
    ))

    # 添加关系
    vrg.add_relationship(VariableEdge(
        source="connection_timeout",
        target="connection_success_rate",
        edge_type=EdgeType.DEPENDENCY,
        weight=0.6,
        description="超时越长，成功率越高"
    ))

    vrg.add_relationship(VariableEdge(
        source="reconnect_delay",
        target="connection_success_rate",
        edge_type=EdgeType.DEPENDENCY,
        weight=-0.4,
        description="延迟越长，成功率越低"
    ))

    vrg.add_relationship(VariableEdge(
        source="connection_success_rate",
        target="stability_score",
        edge_type=EdgeType.INFLUENCE,
        weight=0.8,
        description="成功率直接影响稳定性分数"
    ))

    print("生成变量关系图...")
    vrg.generate(show=False)
    print("✓ 变量关系图已生成")

    # 示例 2: 优化轨迹图
    otg = OptimizationTrajectoryGraph("模拟退火优化轨迹")

    # 添加模拟轨迹点
    for i in range(100):
        point = OptimizationPoint(
            iteration=i,
            variables={
                "connection_timeout": 10 + i * 0.5 + np.random.normal(0, 0.5),
                "reconnect_delay": 5 - i * 0.04 + np.random.normal(0, 0.2),
            },
            objective_value=100 - i * 0.8 + np.random.normal(0, 2),
            is_feasible=True
        )
        otg.add_point(point)

    print("生成优化轨迹图...")
    otg.generate(show=False)
    otg.generate_2d_trajectory("connection_timeout", "reconnect_delay", show=False)
    print("✓ 优化轨迹图已生成")

    # 示例 3: 约束可视化
    cv = ConstraintVisualization()

    def timeout_constraint(timeout):
        return 5 <= timeout <= 60

    print("生成约束可视化...")
    cv.visualize_1d_constraint(
        variable_name="connection_timeout",
        constraint_func=timeout_constraint,
        bounds=(0, 70),
        show=False
    )
    print("✓ 约束可视化已生成")

    # 示例 4: 敏感性分析
    sag = SensitivityAnalysisGraph("蓝牙连接参数敏感性分析")

    sag.add_variable_sensitivity(
        variable_name="connection_timeout",
        perturbations=[-5, -2, -1, 0, 1, 2, 5],
        objective_changes=[15, 6, 3, 0, -3, -6, -15]
    )

    sag.add_variable_sensitivity(
        variable_name="reconnect_delay",
        perturbations=[-2, -1, 0, 1, 2],
        objective_changes=[-8, -4, 0, 4, 8]
    )

    print("生成敏感性分析图...")
    sag.generate(show=False)
    print("✓ 敏感性分析图已生成")

    print("\n所有可视化图表已生成！")
