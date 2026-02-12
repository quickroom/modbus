# modbus
modbus server and client
# Modbus TCP Client and Server

This package contains a Modbus TCP server and client that can communicate across separate networks.

## Requirements

Install the required Python package:

```bash
pip install pymodbus --break-system-packages
```

## Files

- `modbus_server.py` - Modbus TCP server that listens for connections
- `modbus_client.py` - Modbus TCP client that connects to the server
- `README.md` - This file

## Server Setup

### Basic Usage

Start the server on all network interfaces (allows remote connections):

```bash
python3 modbus_server.py
```

This will start the server on `0.0.0.0:5020` (all interfaces, port 5020).

### Custom Configuration

Specify a custom host and port:

```bash
python3 modbus_server.py --host 0.0.0.0 --port 5020
```

### Network Configuration

For cross-network communication, ensure:

1. The server host has a public IP or is accessible via port forwarding
2. Firewall allows incoming connections on the Modbus port (default: 5020)
3. If behind NAT, configure port forwarding: External Port 5020 → Server IP:5020

## Client Setup

### Basic Usage

Connect to a server and run the demo sequence:

```bash
python3 modbus_client.py <SERVER_IP>
```

Replace `<SERVER_IP>` with the actual IP address of your server.

### Custom Port

If the server uses a different port:

```bash
python3 modbus_client.py <SERVER_IP> --port 5020
```

### Interactive Mode

For manual testing with an interactive shell:

```bash
python3 modbus_client.py <SERVER_IP> --interactive
```

Available commands in interactive mode:
- `wc <address> <value>` - Write coil (value: 0 or 1)
- `rc <address> <count>` - Read coils
- `wr <address> <value>` - Write register
- `rr <address> <count>` - Read holding registers
- `ri <address> <count>` - Read input registers
- `demo` - Run demo sequence
- `quit` - Exit

### Demo Mode

Run the built-in demo sequence:

```bash
python3 modbus_client.py <SERVER_IP> --demo
```

## Example Usage

### Scenario 1: Local Testing

**Terminal 1 (Server):**
```bash
python3 modbus_server.py
```

**Terminal 2 (Client):**
```bash
python3 modbus_client.py localhost --demo
```

### Scenario 2: Cross-Network Communication

**Server (on network 192.168.1.0/24):**
```bash
# Server IP: 192.168.1.100
python3 modbus_server.py --host 0.0.0.0 --port 5020
```

**Client (on different network):**
```bash
# Connect to server's public IP or forwarded address
python3 modbus_client.py 203.0.113.50 --port 5020 --interactive
```

### Scenario 3: Using Port Forwarding

If your server is behind NAT:

1. Configure router to forward external port 5020 to server's internal IP:5020
2. Client connects to your public IP address
3. Router forwards traffic to the internal server

## Modbus Functions Supported

### Client Operations

1. **Write Coil** - Write a single digital output (ON/OFF)
2. **Read Coils** - Read digital outputs
3. **Write Register** - Write a single 16-bit register
4. **Read Holding Registers** - Read 16-bit registers (read/write)
5. **Write Multiple Registers** - Write multiple 16-bit registers
6. **Read Input Registers** - Read 16-bit registers (read-only)

### Server Data Store

The server maintains four types of data:

- **Discrete Inputs (di)**: 100 registers (read-only digital inputs)
- **Coils (co)**: 100 registers (read/write digital outputs)
- **Holding Registers (hr)**: 100 registers (read/write 16-bit values)
- **Input Registers (ir)**: 100 registers (read-only 16-bit values)

## Troubleshooting

### Connection Refused

- Check if server is running
- Verify firewall allows connections on port 5020
- Ensure correct IP address and port

### Timeout Errors

- Check network connectivity between client and server
- Verify server is reachable: `ping <SERVER_IP>`
- Ensure no firewall blocking traffic

### Port Already in Use

- Change the port: `python3 modbus_server.py --port 5021`
- Kill existing process using the port

## Security Considerations

**Important**: Modbus TCP has no built-in security or authentication.

For production use:
- Use VPN or SSH tunneling for cross-network communication
- Implement firewall rules to restrict access
- Consider using Modbus TCP with TLS/SSL wrapper
- Don't expose Modbus directly to the internet without protection

## Example VPN/Tunnel Setup

### SSH Tunnel (recommended for secure cross-network communication)

**On client machine:**
```bash
# Create SSH tunnel
ssh -L 5020:localhost:5020 user@server-ip

# In another terminal, connect to localhost
python3 modbus_client.py localhost --port 5020
```

This tunnels the Modbus traffic through an encrypted SSH connection.

## Additional Resources

- Modbus Protocol: https://en.wikipedia.org/wiki/Modbus
- pymodbus Documentation: https://pymodbus.readthedocs.io/
