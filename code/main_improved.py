#!/usr/bin/env python3
"""
Improved main entry point for GeneticA VideoGame Battle
Provides both console and GUI interfaces
"""

import sys
import argparse
import combat.enemy as enemy
import combat.party as party
import combat.combat as combat


def console_interface():
    """Run the enhanced console interface"""
    try:
        from console_enhanced import enhanced_console_interface
        enhanced_console_interface()
    except ImportError:
        # Fallback to original console interface
        original_console_interface()


def original_console_interface():
    """Run the original console interface"""
    sleeping_table = enemy.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()

    party_list = [Makoto, Yukari, Akihiko, Junpei]

    print("Welcome to the Sleeping table combat!")
    print("Select options:")
    print("----------------------")
    menu_finished = False
    while not menu_finished:
        print("1. Start Combat")
        print("2. Simulate combat and print results")
        print("3. Exit")
        print("---------------------")
        choice = input("Enter your choice: ")

        if choice == "1":
            combat.start_combat(party_list, sleeping_table)
            menu_finished = True
        elif choice == "2":
            combat.simulate_combat(party_list, sleeping_table)
            menu_finished = True
        elif choice == "3":
            print("Exiting the game.")
            menu_finished = True
        else:
            print("Invalid choice, try again.")


def gui_interface():
    """Run the improved GUI interface"""
    try:
        import tkinter
        # Test if display is available
        root = tkinter.Tk()
        root.withdraw()  # Hide the test window
        root.destroy()
        
        from gui.main_gui import main as gui_main
        gui_main()
    except tkinter.TclError as e:
        if "no display" in str(e).lower():
            print("Error: No display available for GUI. Falling back to console interface.")
            console_interface()
        else:
            print(f"GUI Error: {e}")
            print("Falling back to console interface.")
            console_interface()
    except ImportError as e:
        print(f"Error: Could not import GUI module: {e}")
        print("GUI requires tkinter. Please make sure it's installed.")
        print("Falling back to console interface.")
        console_interface()
    except Exception as e:
        print(f"Error running GUI: {e}")
        print("Falling back to console interface.")
        console_interface()


def main():
    """Main function with interface selection"""
    parser = argparse.ArgumentParser(
        description='GeneticA VideoGame Battle - Persona 3 Boss Combat Simulator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main_improved.py              # Auto-detect best interface
  python main_improved.py --gui        # Force GUI interface  
  python main_improved.py --console    # Force console interface
        """
    )
    
    parser.add_argument('--gui', action='store_true',
                       help='Force GUI interface')
    parser.add_argument('--console', action='store_true', 
                       help='Force console interface')
    
    args = parser.parse_args()
    
    # Set random seed as in original
    import random
    random.seed(33)  # tu tu tu max verstappen xd
    
    print("Starting the game...")
    
    # Determine which interface to use
    if args.console and args.gui:
        print("Error: Cannot specify both --gui and --console")
        sys.exit(1)
    elif args.console:
        console_interface()
    elif args.gui:
        gui_interface()
    else:
        # Auto-detect: try GUI first, fallback to console
        try:
            import tkinter
            print("GUI available - starting graphical interface...")
            print("(Use --console flag to force console interface)")
            gui_interface()
        except ImportError:
            print("GUI not available - using console interface...")
            console_interface()


if __name__ == "__main__":
    main()