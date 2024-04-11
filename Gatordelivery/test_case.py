import sys
import contextlib
from order_management_system import OrderManagementSystem

def run_test_case(input_filename, output_filename):
    oms = OrderManagementSystem()
    with open(input_filename, 'r') as f:
        lines = f.readlines()

    with open(output_filename, 'w') as f_out:
        with contextlib.redirect_stdout(f_out):
            for line in lines:
                command = line.strip().split('(')[0]
                args_str = line.strip().split('(')[1].rstrip(')')
                args = [int(arg.strip()) for arg in args_str.split(',') if arg.strip()]

                if command == 'createOrder':
                    oms.create_order(*args)
                elif command == 'cancelOrder':
                    oms.cancel_order(*args)
                elif command == 'updateTime':
                    oms.update_time(*args)
                elif command == 'getRankOfOrder':
                    oms.get_rank_of_order(*args)
                elif command == 'print':
                    oms.print_orders_in_time_range(*args)
                elif command == 'Quit':
                    oms.quit()
                    break  # Ensure the script stops processing after Quit

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python script.py input_filename output_filename")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    run_test_case(input_filename, output_filename)
