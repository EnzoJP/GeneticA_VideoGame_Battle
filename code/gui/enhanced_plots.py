"""
Enhanced plotting functionality for GUI integration
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk


class EnhancedPlotter:
    """Enhanced plotter with GUI integration capabilities"""
    
    def __init__(self, parent_frame=None):
        self.parent_frame = parent_frame
        self.figures = []
        
    def create_comparison_plot(self, results_dict, title="Comparación de Algoritmos"):
        """Create a comprehensive comparison plot"""
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(title, fontsize=16, fontweight='bold')
        
        algorithms = list(results_dict.keys())
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
        
        # Win rates
        win_rates = [results_dict[alg].get('win_rate', 0) for alg in algorithms]
        bars1 = ax1.bar(algorithms, win_rates, color=colors[:len(algorithms)])
        ax1.set_title('Tasa de Victoria (%)', fontweight='bold')
        ax1.set_ylabel('Porcentaje (%)')
        ax1.set_ylim(0, 100)
        ax1.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, rate in zip(bars1, win_rates):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # Average turns
        avg_turns = [results_dict[alg].get('avg_turns', 0) for alg in algorithms]
        bars2 = ax2.bar(algorithms, avg_turns, color=colors[:len(algorithms)])
        ax2.set_title('Promedio de Turnos', fontweight='bold')
        ax2.set_ylabel('Turnos')
        ax2.grid(True, alpha=0.3)
        
        for bar, turns in zip(bars2, avg_turns):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{turns:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # Average damage done
        avg_damage_done = [results_dict[alg].get('avg_damage_done', 0) for alg in algorithms]
        bars3 = ax3.bar(algorithms, avg_damage_done, color=colors[:len(algorithms)])
        ax3.set_title('Daño Promedio Realizado', fontweight='bold')
        ax3.set_ylabel('Puntos de Daño')
        ax3.grid(True, alpha=0.3)
        
        for bar, damage in zip(bars3, avg_damage_done):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{damage:.0f}', ha='center', va='bottom', fontweight='bold')
        
        # Execution time
        exec_times = [results_dict[alg].get('execution_time', 0) for alg in algorithms]
        bars4 = ax4.bar(algorithms, exec_times, color=colors[:len(algorithms)])
        ax4.set_title('Tiempo de Ejecución', fontweight='bold')
        ax4.set_ylabel('Segundos')
        ax4.grid(True, alpha=0.3)
        
        for bar, time_val in zip(bars4, exec_times):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{time_val:.2f}s', ha='center', va='bottom', fontweight='bold')
        
        # Rotate x-axis labels for better readability
        for ax in [ax1, ax2, ax3, ax4]:
            ax.tick_params(axis='x', rotation=15)
            
        plt.tight_layout()
        self.figures.append(fig)
        return fig
    
    def create_performance_radar(self, results_dict):
        """Create a radar chart comparing algorithm performance"""
        algorithms = list(results_dict.keys())
        metrics = ['Win Rate', 'Avg Turns', 'Damage Done', 'Speed']
        
        # Normalize metrics to 0-1 scale for radar chart
        normalized_data = {}
        for alg in algorithms:
            data = results_dict[alg]
            normalized_data[alg] = [
                data.get('win_rate', 0) / 100,  # Win rate (0-100% -> 0-1)
                1 - (data.get('avg_turns', 50) / 100),  # Fewer turns is better (invert)
                data.get('avg_damage_done', 0) / 1000,  # Damage (normalize to reasonable scale)
                1 - (data.get('execution_time', 10) / 10)  # Faster is better (invert)
            ]
        
        # Create radar chart
        angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
        
        for i, (alg, data) in enumerate(normalized_data.items()):
            values = data + data[:1]  # Complete the circle
            ax.plot(angles, values, 'o-', linewidth=2, label=alg, color=colors[i % len(colors)])
            ax.fill(angles, values, alpha=0.25, color=colors[i % len(colors)])
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics)
        ax.set_ylim(0, 1)
        ax.set_title('Comparación de Rendimiento (Radar)', size=16, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        ax.grid(True)
        
        plt.tight_layout()
        self.figures.append(fig)
        return fig
    
    def embed_in_tkinter(self, figure, parent_widget):
        """Embed a matplotlib figure in a tkinter widget"""
        if self.parent_frame is None:
            self.parent_frame = parent_widget
            
        canvas = FigureCanvasTkAgg(figure, parent_widget)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Add toolbar
        toolbar_frame = ttk.Frame(parent_widget)
        toolbar_frame.pack(fill='x')
        
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        
        return canvas
    
    def save_all_figures(self, directory="plots"):
        """Save all created figures to files"""
        import os
        os.makedirs(directory, exist_ok=True)
        
        for i, fig in enumerate(self.figures):
            filename = f"{directory}/comparison_plot_{i+1}.png"
            fig.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Saved plot to {filename}")
    
    def clear_figures(self):
        """Clear all stored figures"""
        for fig in self.figures:
            plt.close(fig)
        self.figures.clear()


def create_sample_results():
    """Create sample results for testing"""
    return {
        'Random': {
            'win_rate': 25.5,
            'avg_turns': 15.2,
            'avg_damage_done': 450,
            'execution_time': 0.5
        },
        'Genetic': {
            'win_rate': 78.3,
            'avg_turns': 12.1,
            'avg_damage_done': 620,
            'execution_time': 2.3
        },
        'Modified Genetic': {
            'win_rate': 85.7,
            'avg_turns': 10.8,
            'avg_damage_done': 680,
            'execution_time': 2.8
        },
        'NSGA-II': {
            'win_rate': 92.1,
            'avg_turns': 9.5,
            'avg_damage_done': 720,
            'execution_time': 4.2
        }
    }


if __name__ == "__main__":
    # Test the plotting functionality
    plotter = EnhancedPlotter()
    sample_data = create_sample_results()
    
    fig1 = plotter.create_comparison_plot(sample_data)
    fig2 = plotter.create_performance_radar(sample_data)
    
    plt.show()