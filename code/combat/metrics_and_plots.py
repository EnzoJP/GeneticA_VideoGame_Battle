import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import rcParams

# Configurar estilo de gráficos
plt.style.use('seaborn-v0_8')
rcParams['figure.figsize'] = (12, 8)
rcParams['font.size'] = 12

def plot_comparative_results(results_dict, metric_name, title, ylabel, save_path=None):
    """
    Args:
        results_dict: Dictionary with algorithm as key and list of values as value
        metric_name: Name of the metric to visualize
        title: Title of the plot
        ylabel: Y-axis label
        save_path: Path to save the image (optional)
    """
    algorithms = list(results_dict.keys())
    data = list(results_dict.values())
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    boxplot = ax.boxplot(data, labels=algorithms, patch_artist=True) #Box plot
    
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink']
    for patch, color in zip(boxplot['boxes'], colors):
        patch.set_facecolor(color)

    # Add individual data points
    for i, algorithm in enumerate(algorithms):
        y = results_dict[algorithm]
        x = np.random.normal(i + 1, 0.04, size=len(y))
        ax.plot(x, y, 'r.', alpha=0.4)
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=14)
    ax.grid(True, alpha=0.3)

    # Adjust layout
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()

def plot_win_rate_comparison(win_rates_dict, title="Comparación de Tasas de Victoria", save_path=None): # Makes a bar plot to compare win rates
    """
    Args:
        win_rates_dict: Dictionary with algorithm as key and win rate as value
        title: Title of the plot
        save_path: Path to save the image (optional)
    """
    algorithms = list(win_rates_dict.keys())
    win_rates = list(win_rates_dict.values())
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.bar(algorithms, win_rates, color=['skyblue', 'lightgreen', 'salmon', 'gold'])
    
    # Add value annotations to bars
    for bar, rate in zip(bars, win_rates):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{rate:.2f}%', ha='center', va='bottom', fontweight='bold')
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_ylabel('Tasa de Victoria (%)', fontsize=14)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()

def create_all_comparative_plots(results, save_directory=None):
    """
    Args:
        results: Diccionario with every result
        save_directory: directory to save the images (optional)
    """
    # Extract data for each metric
    turns_data = {algo: results[algo]['turns'] for algo in results}
    damage_done_data = {algo: results[algo]['damage_done'] for algo in results}
    damage_taken_data = {algo: results[algo]['damage_taken'] for algo in results}
    deaths_data = {algo: results[algo]['deaths'] for algo in results}
    win_rates = {algo: results[algo]['win_rate'] for algo in results}

    # Create comparative plots
    plot_comparative_results(
        turns_data, 
        "turns", 
        "Comparación de Turnos por Algoritmo", 
        "Número de Turnos",
        save_path=f"{save_directory}/turns_comparison.png" if save_directory else None
    )
    
    plot_comparative_results(
        damage_done_data, 
        "damage_done", 
        "Comparación de Daño Infligido por Algoritmo", 
        "Daño Infligido",
        save_path=f"{save_directory}/damage_done_comparison.png" if save_directory else None
    )
    
    plot_comparative_results(
        damage_taken_data, 
        "damage_taken", 
        "Comparación de Daño Recibido por Algoritmo", 
        "Daño Recibido",
        save_path=f"{save_directory}/damage_taken_comparison.png" if save_directory else None
    )
    
    plot_comparative_results(
        deaths_data, 
        "deaths", 
        "Comparación de Muertes por Algoritmo", 
        "Número de Muertes",
        save_path=f"{save_directory}/deaths_comparison.png" if save_directory else None
    )
    
    plot_win_rate_comparison(
        win_rates,
        "Comparación de Tasas de Victoria por Algoritmo",
        save_path=f"{save_directory}/win_rate_comparison.png" if save_directory else None
    )

def record_combat(damage_done, damage_taken, turns, won): 
    #combat stats
    return {
        "damage_done": damage_done,
        "damage_taken": damage_taken,
        "turns": turns,
        "won": won
    }

def calculate_win_rate (wins, losses):
    """Calculate the win rate as a percentage."""
    total = wins + losses
    if total == 0:
        return 0.0
    return (wins / total) * 100




