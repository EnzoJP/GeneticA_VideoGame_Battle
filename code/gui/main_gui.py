import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Import existing modules
import combat.enemy as enemy
import combat.party as party
import combat.combat as combat
from gui.enhanced_plots import EnhancedPlotter


class GeneticBattleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GeneticA VideoGame Battle - Persona 3")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # Initialize game objects
        self.sleeping_table = enemy.Enemy()
        self.makoto = party.Makoto()
        self.yukari = party.Yukari()
        self.akihiko = party.Akihiko()
        self.junpei = party.Junpei()
        self.party_list = [self.makoto, self.yukari, self.akihiko, self.junpei]
        
        # Initialize plotter
        self.plotter = EnhancedPlotter()
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        """Setup custom styles for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', 
                       font=('Arial', 18, 'bold'),
                       background='#2c3e50',
                       foreground='#ecf0f1')
        
        style.configure('Subtitle.TLabel',
                       font=('Arial', 12, 'bold'),
                       background='#2c3e50', 
                       foreground='#bdc3c7')
        
        style.configure('Custom.TButton',
                       font=('Arial', 11),
                       padding=10)
        
        style.configure('Action.TButton',
                       font=('Arial', 10, 'bold'),
                       padding=(15, 8))
        
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="GeneticA VideoGame Battle", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame,
                                 text="Algoritmos Genéticos para vencer al jefe 'Sleeping Table' de Persona 3",
                                 style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_main_tab()
        self.create_simulation_tab()
        self.create_results_tab()
        
    def create_main_tab(self):
        """Create the main menu tab"""
        main_tab = ttk.Frame(self.notebook)
        self.notebook.add(main_tab, text="Menú Principal")
        
        # Welcome message
        welcome_frame = ttk.LabelFrame(main_tab, text="Bienvenido", padding=20)
        welcome_frame.pack(fill='x', padx=20, pady=20)
        
        welcome_text = """¡Bienvenido al combate contra la Sleeping Table!
        
Este sistema utiliza algoritmos genéticos para encontrar la mejor estrategia de combate.
Puedes elegir entre jugar manualmente o simular combates automáticos."""
        
        ttk.Label(welcome_frame, text=welcome_text, justify='left').pack()
        
        # Action buttons frame
        buttons_frame = ttk.Frame(main_tab)
        buttons_frame.pack(expand=True)
        
        # Start Combat button
        ttk.Button(buttons_frame,
                  text="🎮 Iniciar Combate Manual",
                  style='Action.TButton',
                  command=self.start_manual_combat).pack(pady=10, fill='x')
        
        # Simulate Combat button  
        ttk.Button(buttons_frame,
                  text="🤖 Simular Combate con IA",
                  style='Action.TButton', 
                  command=self.show_simulation_tab).pack(pady=10, fill='x')
        
        # Exit button
        ttk.Button(buttons_frame,
                  text="❌ Salir",
                  style='Action.TButton',
                  command=self.root.quit).pack(pady=10, fill='x')
                  
    def create_simulation_tab(self):
        """Create the simulation configuration tab"""
        sim_tab = ttk.Frame(self.notebook)
        self.notebook.add(sim_tab, text="Simulación de Algoritmos")
        
        # Algorithm selection frame
        algo_frame = ttk.LabelFrame(sim_tab, text="Seleccionar Algoritmo", padding=20)
        algo_frame.pack(fill='x', padx=20, pady=20)
        
        self.algorithm_var = tk.StringVar(value="compare_all")
        
        algorithms = [
            ("🎲 Algoritmo Aleatorio", "random"),
            ("🧬 Algoritmo Genético Básico", "genetic"),
            ("🧬+ Algoritmo Genético Modificado", "modified_genetic"),
            ("🔬 NSGA-II", "nsga2"),
            ("📊 Comparar Todos los Algoritmos", "compare_all")
        ]
        
        for text, value in algorithms:
            ttk.Radiobutton(algo_frame, text=text, variable=self.algorithm_var, 
                           value=value).pack(anchor='w', pady=5)
        
        # Configuration frame
        config_frame = ttk.LabelFrame(sim_tab, text="Configuración", padding=20)
        config_frame.pack(fill='x', padx=20, pady=20)
        
        # Number of simulations
        ttk.Label(config_frame, text="Número de simulaciones:").pack(anchor='w')
        self.simulations_var = tk.StringVar(value="10")
        ttk.Entry(config_frame, textvariable=self.simulations_var, width=10).pack(anchor='w', pady=(0, 10))
        
        # Save plots checkbox
        self.save_plots_var = tk.BooleanVar(value=False)
        ttk.Checkbox(config_frame, text="Guardar gráficos", 
                    variable=self.save_plots_var).pack(anchor='w')
        
        # Run simulation button
        ttk.Button(sim_tab,
                  text="▶️ Ejecutar Simulación",
                  style='Action.TButton',
                  command=self.run_simulation).pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(sim_tab, mode='indeterminate')
        self.progress.pack(fill='x', padx=20, pady=10)
        
    def create_results_tab(self):
        """Create the results display tab"""
        results_tab = ttk.Frame(self.notebook)
        self.notebook.add(results_tab, text="Resultados")
        
        # Create paned window for results and plots
        paned = ttk.PanedWindow(results_tab, orient='vertical')
        paned.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Results text frame
        text_frame = ttk.LabelFrame(paned, text="Resultados de Simulación")
        paned.add(text_frame, weight=1)
        
        self.results_text = scrolledtext.ScrolledText(text_frame, height=15, font=('Consolas', 10))
        self.results_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Plots frame
        plots_frame = ttk.LabelFrame(paned, text="Gráficos de Comparación")
        paned.add(plots_frame, weight=2)
        
        # Create notebook for different plot types
        self.plots_notebook = ttk.Notebook(plots_frame)
        self.plots_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Comparison plots tab
        self.comparison_frame = ttk.Frame(self.plots_notebook)
        self.plots_notebook.add(self.comparison_frame, text="Comparación Detallada")
        
        # Radar chart tab
        self.radar_frame = ttk.Frame(self.plots_notebook)
        self.plots_notebook.add(self.radar_frame, text="Gráfico Radar")
        
        # Clear plots button
        ttk.Button(plots_frame, text="🗑️ Limpiar Gráficos", 
                  command=self.clear_plots).pack(pady=5)
        
    def show_simulation_tab(self):
        """Switch to simulation tab"""
        self.notebook.select(1)
        
    def start_manual_combat(self):
        """Start manual combat in a separate thread"""
        def run_manual_combat():
            try:
                # Redirect output to capture it
                output_buffer = io.StringIO()
                with redirect_stdout(output_buffer), redirect_stderr(output_buffer):
                    combat.start_combat(self.party_list, self.sleeping_table)
                
                # Display results
                self.show_results(output_buffer.getvalue())
                
            except Exception as e:
                messagebox.showerror("Error", f"Error durante el combate: {str(e)}")
                
        # Show progress and run in thread
        self.progress.start()
        threading.Thread(target=run_manual_combat, daemon=True).start()
        
    def run_simulation(self):
        """Run the selected simulation"""
        def simulate():
            try:
                self.progress.start()
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "Ejecutando simulación...\n")
                self.results_text.update()
                
                # Get configuration
                algorithm = self.algorithm_var.get()
                n_simulations = int(self.simulations_var.get() or "10")
                save_plots = self.save_plots_var.get()
                
                # Capture output
                output_buffer = io.StringIO()
                
                with redirect_stdout(output_buffer), redirect_stderr(output_buffer):
                    if algorithm == "compare_all":
                        combat.compare_all_algorithms(n_simulations, save_plots)
                    else:
                        # Run single algorithm simulation
                        self.run_single_algorithm(algorithm, n_simulations)
                
                # Show results
                results = output_buffer.getvalue()
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, results)
                
                # Generate sample plots for demonstration
                self.generate_sample_plots()
                
                # Switch to results tab
                self.notebook.select(2)
                
            except Exception as e:
                self.results_text.insert(tk.END, f"\nError: {str(e)}\n")
                messagebox.showerror("Error", f"Error durante la simulación: {str(e)}")
            finally:
                self.progress.stop()
                
        threading.Thread(target=simulate, daemon=True).start()
        
    def run_single_algorithm(self, algorithm, n_simulations):
        """Run a single algorithm simulation"""
        # This would implement the logic for running individual algorithms
        # For now, just run the compare_all to get some results
        combat.compare_all_algorithms(n_simulations, self.save_plots_var.get())
        
    def show_results(self, results):
        """Display results in the results tab"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, results)
        self.notebook.select(2)
        self.progress.stop()
        
    def generate_sample_plots(self):
        """Generate sample plots for demonstration"""
        try:
            # Clear previous plots
            self.clear_plots()
            
            # Create sample data (in a real scenario, this would come from actual results)
            from gui.enhanced_plots import create_sample_results
            sample_data = create_sample_results()
            
            # Create comparison plot
            fig1 = self.plotter.create_comparison_plot(sample_data, "Resultados de Simulación")
            self.plotter.embed_in_tkinter(fig1, self.comparison_frame)
            
            # Create radar chart
            fig2 = self.plotter.create_performance_radar(sample_data)
            self.plotter.embed_in_tkinter(fig2, self.radar_frame)
            
        except Exception as e:
            print(f"Error generating plots: {e}")
            
    def clear_plots(self):
        """Clear all plots from the GUI"""
        # Clear the frames
        for widget in self.comparison_frame.winfo_children():
            widget.destroy()
        for widget in self.radar_frame.winfo_children():
            widget.destroy()
            
        # Clear plotter figures
        self.plotter.clear_figures()


def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = GeneticBattleGUI(root)
    
    # Set random seed as in original
    import random
    random.seed(33)
    
    root.mainloop()


if __name__ == "__main__":
    main()