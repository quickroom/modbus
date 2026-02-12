#!/usr/bin/env python3
"""
Modbus TCP Client
Connects to a Modbus server on a separate network and sends/receives data.
"""

from pymodbus.client import ModbusTcpClient
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)


class ModbusClientApp:
    def __init__(self, host, port=5020):
        """
        Initialize Modbus client.
        
        Args:
            host: IP address or hostname of the Modbus server
            port: Port number of the Modbus server (default: 5020)
        """
        self.host = host
        self.port = port
        self.client = ModbusTcpClient(host=host, port=port, timeout=3)
        
    def connect(self):
        """Establish connection to the server."""
        log.info(f"Connecting to Modbus server at {self.host}:{self.port}")
        result = self.client.connect()
        if result:
            log.info("Successfully connected to server")
        else:
            log.error("Failed to connect to server")
        return result
    
    def disconnect(self):
        """Close connection to the server."""
        self.client.close()
        log.info("Disconnected from server")
    
    def write_coil(self, address, value):
        """
        Write a single coil (digital output).
        
        Args:
            address: Register address (0-based)
            value: Boolean value (True/False)
        """
        try:
            result = self.client.write_coil(address, value)
            if not result.isError():
                log.info(f"Successfully wrote coil at address {address}: {value}")
                return True
            else:
                log.error(f"Error writing coil: {result}")
                return False
        except Exception as e:
            log.error(f"Exception writing coil: {e}")
            return False
    
    def read_coils(self, address, count=1):
        """
        Read coils (digital outputs).
        
        Args:
            address: Starting register address
            count: Number of coils to read
        """
        try:
            result = self.client.read_coils(address, count)
            if not result.isError():
                log.info(f"Read coils from address {address}: {result.bits[:count]}")
                return result.bits[:count]
            else:
                log.error(f"Error reading coils: {result}")
                return None
        except Exception as e:
            log.error(f"Exception reading coils: {e}")
            return None
    
    def write_register(self, address, value):
        """
        Write a single holding register.
        
        Args:
            address: Register address (0-based)
            value: Integer value (0-65535)
        """
        try:
            result = self.client.write_register(address, value)
            if not result.isError():
                log.info(f"Successfully wrote register at address {address}: {value}")
                return True
            else:
                log.error(f"Error writing register: {result}")
                return False
        except Exception as e:
            log.error(f"Exception writing register: {e}")
            return False
    
    def read_holding_registers(self, address, count=1):
        """
        Read holding registers.
        
        Args:
            address: Starting register address
            count: Number of registers to read
        """
        try:
            result = self.client.read_holding_registers(address, count)
            if not result.isError():
                log.info(f"Read holding registers from address {address}: {result.registers}")
                return result.registers
            else:
                log.error(f"Error reading holding registers: {result}")
                return None
        except Exception as e:
            log.error(f"Exception reading holding registers: {e}")
            return None
    
    def write_multiple_registers(self, address, values):
        """
        Write multiple holding registers.
        
        Args:
            address: Starting register address
            values: List of integer values
        """
        try:
            result = self.client.write_registers(address, values)
            if not result.isError():
                log.info(f"Successfully wrote {len(values)} registers starting at address {address}")
                return True
            else:
                log.error(f"Error writing multiple registers: {result}")
                return False
        except Exception as e:
            log.error(f"Exception writing multiple registers: {e}")
            return False
    
    def read_input_registers(self, address, count=1):
        """
        Read input registers.
        
        Args:
            address: Starting register address
            count: Number of registers to read
        """
        try:
            result = self.client.read_input_registers(address, count)
            if not result.isError():
                log.info(f"Read input registers from address {address}: {result.registers}")
                return result.registers
            else:
                log.error(f"Error reading input registers: {result}")
                return None
        except Exception as e:
            log.error(f"Exception reading input registers: {e}")
            return None


def demo_communication(client):
    """
    Demonstrate basic Modbus communication.
    
    Args:
        client: ModbusClientApp instance
    """
    log.info("\n=== Starting Modbus Communication Demo ===\n")
    
    # Write and read coils
    log.info("--- Testing Coils (Digital Outputs) ---")
    client.write_coil(0, True)
    time.sleep(0.1)
    client.read_coils(0, 1)
    
    # Write and read holding registers
    log.info("\n--- Testing Holding Registers ---")
    client.write_register(0, 1234)
    time.sleep(0.1)
    client.read_holding_registers(0, 1)
    
    # Write and read multiple registers
    log.info("\n--- Testing Multiple Registers ---")
    client.write_multiple_registers(10, [100, 200, 300, 400, 500])
    time.sleep(0.1)
    client.read_holding_registers(10, 5)
    
    log.info("\n=== Demo Complete ===\n")


def interactive_mode(client):
    """
    Interactive mode for manual testing.
    
    Args:
        client: ModbusClientApp instance
    """
    print("\n=== Interactive Modbus Client ===")
    print("Commands:")
    print("  wc <address> <value>    - Write coil (value: 0 or 1)")
    print("  rc <address> <count>    - Read coils")
    print("  wr <address> <value>    - Write register")
    print("  rr <address> <count>    - Read holding registers")
    print("  ri <address> <count>    - Read input registers")
    print("  demo                    - Run demo sequence")
    print("  quit                    - Exit")
    print()
    
    while True:
        try:
            cmd = input("modbus> ").strip().split()
            if not cmd:
                continue
            
            if cmd[0] == 'quit':
                break
            elif cmd[0] == 'demo':
                demo_communication(client)
            elif cmd[0] == 'wc' and len(cmd) >= 3:
                client.write_coil(int(cmd[1]), bool(int(cmd[2])))
            elif cmd[0] == 'rc' and len(cmd) >= 3:
                client.read_coils(int(cmd[1]), int(cmd[2]))
            elif cmd[0] == 'wr' and len(cmd) >= 3:
                client.write_register(int(cmd[1]), int(cmd[2]))
            elif cmd[0] == 'rr' and len(cmd) >= 3:
                client.read_holding_registers(int(cmd[1]), int(cmd[2]))
            elif cmd[0] == 'ri' and len(cmd) >= 3:
                client.read_input_registers(int(cmd[1]), int(cmd[2]))
            else:
                print("Invalid command or missing arguments")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Modbus TCP Client')
    parser.add_argument('host', help='IP address or hostname of the Modbus server')
    parser.add_argument('--port', type=int, default=5020,
                       help='Port of the Modbus server (default: 5020)')
    parser.add_argument('--demo', action='store_true',
                       help='Run demo sequence and exit')
    parser.add_argument('--interactive', action='store_true',
                       help='Start in interactive mode')
    
    args = parser.parse_args()
    
    # Create client instance
    client = ModbusClientApp(args.host, args.port)
    
    try:
        # Connect to server
        if not client.connect():
            log.error("Could not connect to server. Exiting.")
            exit(1)
        
        # Run demo or interactive mode
        if args.demo:
            demo_communication(client)
        elif args.interactive:
            interactive_mode(client)
        else:
            # Default: run demo
            demo_communication(client)
            
    except KeyboardInterrupt:
        log.info("\nClient stopped by user")
    except Exception as e:
        log.error(f"Client error: {e}")
    finally:
        client.disconnect()
