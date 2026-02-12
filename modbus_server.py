#!/usr/bin/env python3
"""
Modbus TCP Server
Listens for connections from Modbus clients on separate networks.
"""

from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)


def run_server(host='0.0.0.0', port=5020):
    """
    Start the Modbus TCP server.
    
    Args:
        host: IP address to bind to (0.0.0.0 allows connections from any network)
        port: Port number to listen on (default: 5020)
    """
    
    # Initialize data store
    # Create data blocks for different register types
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0] * 100),    # Discrete Inputs
        co=ModbusSequentialDataBlock(0, [0] * 100),    # Coils
        hr=ModbusSequentialDataBlock(0, [0] * 100),    # Holding Registers
        ir=ModbusSequentialDataBlock(0, [0] * 100)     # Input Registers
    )
    
    # Create server context with single slave
    context = ModbusServerContext(slaves=store, single=True)
    
    # Server identification
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Custom Modbus Server'
    identity.ProductCode = 'MBS'
    identity.VendorUrl = 'http://github.com'
    identity.ProductName = 'Modbus TCP Server'
    identity.ModelName = 'Modbus Server'
    identity.MajorMinorRevision = '1.0.0'
    
    log.info(f"Starting Modbus TCP Server on {host}:{port}")
    log.info("Server will accept connections from remote networks")
    log.info("Press Ctrl+C to stop the server")
    
    # Start the server
    StartTcpServer(
        context=context,
        identity=identity,
        address=(host, port)
    )


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Modbus TCP Server')
    parser.add_argument('--host', default='0.0.0.0', 
                       help='IP address to bind to (default: 0.0.0.0 for all interfaces)')
    parser.add_argument('--port', type=int, default=5020,
                       help='Port to listen on (default: 5020)')
    
    args = parser.parse_args()
    
    try:
        run_server(host=args.host, port=args.port)
    except KeyboardInterrupt:
        log.info("Server stopped by user")
    except Exception as e:
        log.error(f"Server error: {e}")
