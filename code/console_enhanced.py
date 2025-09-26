"""
Enhanced console interface with better formatting and user experience
"""

import os
import sys
import time
from datetime import datetime
import combat.enemy as enemy
import combat.party as party
import combat.combat as combat


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """Print an enhanced banner"""
    banner = f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                    GeneticA VideoGame Battle - Persona 3                     ║
║                                                                              ║
║           Algoritmos Genéticos para vencer al jefe 'Sleeping Table'         ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.ENDC}"""
    print(banner)


def print_menu():
    """Print an enhanced menu"""
    menu = f"""
{Colors.OKBLUE}{Colors.BOLD}🎮 MENÚ PRINCIPAL {Colors.ENDC}
{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}

{Colors.OKGREEN}1.{Colors.ENDC} {Colors.BOLD}🎯 Iniciar Combate Manual{Colors.ENDC}
   Juega el combate paso a paso, eligiendo las acciones de cada personaje

{Colors.OKGREEN}2.{Colors.ENDC} {Colors.BOLD}🤖 Simular Combate con IA{Colors.ENDC}
   Ejecuta simulaciones automáticas usando algoritmos genéticos

{Colors.OKGREEN}3.{Colors.ENDC} {Colors.BOLD}📊 Ver Información del Sistema{Colors.ENDC}
   Muestra detalles sobre los algoritmos y personajes

{Colors.OKGREEN}4.{Colors.ENDC} {Colors.BOLD}❌ Salir{Colors.ENDC}
   Cierra la aplicación

{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}
"""
    print(menu)


def print_simulation_menu():
    """Print the simulation algorithm selection menu"""
    menu = f"""
{Colors.OKBLUE}{Colors.BOLD}🤖 SELECCIÓN DE ALGORITMO {Colors.ENDC}
{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}

{Colors.OKGREEN}1.{Colors.ENDC} {Colors.BOLD}🎲 Algoritmo Aleatorio{Colors.ENDC}
   Selecciona acciones al azar (línea base)

{Colors.OKGREEN}2.{Colors.ENDC} {Colors.BOLD}🧬 Algoritmo Genético Básico{Colors.ENDC}
   Implementación estándar del algoritmo genético

{Colors.OKGREEN}3.{Colors.ENDC} {Colors.BOLD}🧬+ Algoritmo Genético Modificado{Colors.ENDC}
   Versión mejorada adaptada al problema

{Colors.OKGREEN}4.{Colors.ENDC} {Colors.BOLD}🔬 NSGA-II{Colors.ENDC}
   Algoritmo genético multi-objetivo

{Colors.OKGREEN}5.{Colors.ENDC} {Colors.BOLD}📊 Comparar Todos los Algoritmos{Colors.ENDC}
   Ejecuta todos los algoritmos y compara resultados

{Colors.OKGREEN}6.{Colors.ENDC} {Colors.BOLD}🔙 Volver al Menú Principal{Colors.ENDC}

{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}
"""
    print(menu)


def print_info():
    """Print system information"""
    info = f"""
{Colors.OKBLUE}{Colors.BOLD}📊 INFORMACIÓN DEL SISTEMA {Colors.ENDC}
{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}

{Colors.BOLD}👥 Personajes del Partido:{Colors.ENDC}
• Makoto (Protagonista) - Líder del grupo
• Yukari - Especialista en viento y curación  
• Akihiko - Combatiente cuerpo a cuerpo
• Junpei - Atacante con fuego

{Colors.BOLD}👹 Enemigo:{Colors.ENDC}
• Sleeping Table - Jefe final con múltiples habilidades

{Colors.BOLD}🧬 Algoritmos Disponibles:{Colors.ENDC}
• {Colors.OKGREEN}Aleatorio:{Colors.ENDC} Línea base para comparaciones
• {Colors.OKGREEN}Genético Básico:{Colors.ENDC} Implementación estándar del algoritmo genético
• {Colors.OKGREEN}Genético Modificado:{Colors.ENDC} Versión optimizada para este problema
• {Colors.OKGREEN}NSGA-II:{Colors.ENDC} Algoritmo multi-objetivo para optimización avanzada

{Colors.BOLD}📈 Métricas Evaluadas:{Colors.ENDC}
• Tasa de victoria (%)
• Promedio de turnos por combate
• Daño realizado y recibido
• Tiempo de ejecución
• Número de muertes en el partido

{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}
"""
    print(info)


def get_user_input(prompt, valid_options):
    """Get user input with validation"""
    while True:
        try:
            choice = input(f"{Colors.BOLD}{prompt}{Colors.ENDC}").strip()
            if choice in valid_options:
                return choice
            else:
                print(f"{Colors.FAIL}❌ Opción inválida. Por favor, elige una opción válida: {', '.join(valid_options)}{Colors.ENDC}")
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}⚠️  Operación cancelada por el usuario{Colors.ENDC}")
            return None
        except EOFError:
            print(f"\n{Colors.WARNING}⚠️  Fin de entrada detectado{Colors.ENDC}")
            return None


def get_simulation_config():
    """Get simulation configuration from user"""
    print(f"\n{Colors.OKBLUE}{Colors.BOLD}⚙️  CONFIGURACIÓN DE SIMULACIÓN{Colors.ENDC}")
    print(f"{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}")
    
    # Number of simulations
    while True:
        try:
            n_sim = input(f"{Colors.BOLD}Número de simulaciones por algoritmo (default: 10): {Colors.ENDC}").strip()
            if not n_sim:
                n_sim = 10
                break
            n_sim = int(n_sim)
            if n_sim > 0:
                break
            else:
                print(f"{Colors.FAIL}❌ Por favor, ingresa un número positivo{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}❌ Por favor, ingresa un número válido{Colors.ENDC}")
    
    # Save plots
    save_plots = get_user_input("¿Guardar gráficos? (y/n, default: n): ", ['y', 'n', 'Y', 'N', ''])
    if save_plots is None:
        return None, None
    save_plots = save_plots.lower() == 'y'
    
    return n_sim, save_plots


def run_with_progress(func, description):
    """Run a function with a simple progress indicator"""
    print(f"\n{Colors.OKBLUE}🔄 {description}...{Colors.ENDC}")
    
    import threading
    import time
    
    # Progress animation
    def animate():
        chars = "|/-\\"
        idx = 0
        while not stop_animation:
            print(f"\r{Colors.OKCYAN}{chars[idx % len(chars)]} Procesando...{Colors.ENDC}", end='', flush=True)
            idx += 1
            time.sleep(0.1)
    
    stop_animation = False
    animation_thread = threading.Thread(target=animate)
    animation_thread.daemon = True
    animation_thread.start()
    
    try:
        result = func()
        return result
    finally:
        stop_animation = True
        animation_thread.join(timeout=0.1)
        print(f"\r{Colors.OKGREEN}✅ {description} completado{Colors.ENDC}" + " " * 20)


def enhanced_console_interface():
    """Run the enhanced console interface"""
    # Initialize game objects
    sleeping_table = enemy.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_list = [Makoto, Yukari, Akihiko, Junpei]
    
    while True:
        clear_screen()
        print_banner()
        print_menu()
        
        choice = get_user_input("👉 Selecciona una opción (1-4): ", ['1', '2', '3', '4'])
        
        if choice is None:  # User interrupted
            break
        elif choice == '1':
            print(f"\n{Colors.OKGREEN}🎯 Iniciando combate manual...{Colors.ENDC}")
            print("Presiona Enter para continuar...")
            input()
            
            def start_combat():
                combat.start_combat(party_list, sleeping_table)
            
            run_with_progress(start_combat, "Ejecutando combate manual")
            
            print(f"\n{Colors.OKGREEN}✅ Combate completado{Colors.ENDC}")
            input("Presiona Enter para continuar...")
            
        elif choice == '2':
            while True:
                clear_screen()
                print_banner()
                print_simulation_menu()
                
                sim_choice = get_user_input("👉 Selecciona un algoritmo (1-6): ", ['1', '2', '3', '4', '5', '6'])
                
                if sim_choice is None or sim_choice == '6':
                    break
                    
                # Get simulation configuration
                n_sim, save_plots = get_simulation_config()
                if n_sim is None:
                    continue
                
                print(f"\n{Colors.OKBLUE}🚀 Iniciando simulación...{Colors.ENDC}")
                start_time = time.time()
                
                if sim_choice == '5':  # Compare all algorithms
                    def run_comparison():
                        combat.compare_all_algorithms(n_sim, save_plots)
                    
                    run_with_progress(run_comparison, "Comparando todos los algoritmos")
                else:
                    def run_single_sim():
                        combat.simulate_combat(party_list, sleeping_table)
                    
                    algorithm_names = {
                        '1': 'Algoritmo Aleatorio',
                        '2': 'Algoritmo Genético Básico', 
                        '3': 'Algoritmo Genético Modificado',
                        '4': 'NSGA-II'
                    }
                    
                    run_with_progress(run_single_sim, f"Ejecutando {algorithm_names[sim_choice]}")
                
                end_time = time.time()
                print(f"\n{Colors.OKGREEN}⏱️  Tiempo total de ejecución: {end_time - start_time:.2f} segundos{Colors.ENDC}")
                print(f"\n{Colors.OKGREEN}✅ Simulación completada{Colors.ENDC}")
                input("Presiona Enter para continuar...")
                
        elif choice == '3':
            clear_screen()
            print_banner()
            print_info()
            input("\nPresiona Enter para continuar...")
            
        elif choice == '4':
            print(f"\n{Colors.OKGREEN}👋 ¡Gracias por usar GeneticA VideoGame Battle!{Colors.ENDC}")
            print(f"{Colors.OKCYAN}Hasta la vista, baby! 🤖{Colors.ENDC}")
            break


if __name__ == "__main__":
    enhanced_console_interface()