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

# 🔌 Electrical Plant Register & Command Reference

This Modbus server simulates a simple electrical feeder / plant with breaker control, voltage regulation, load demand, and protection logic.

All values are stored as **scaled integers** (common in real Modbus devices).

---

# 📘 Modbus Data Model Overview

The server maintains four Modbus data areas:

| Type | Access | Description |
|------|--------|-------------|
| **Coils (co)** | Read/Write | Digital control commands |
| **Discrete Inputs (di)** | Read-Only | Status + alarm signals |
| **Holding Registers (hr)** | Read/Write | Operator setpoints |
| **Input Registers (ir)** | Read-Only | Real-time electrical measurements |

---

# ⚡ Electrical Plant Memory Map

---

## 🟢 Coils (Digital Outputs – Controls)

Use command:
`wc address 0|1`

| Address | Name | Description |
|----------|------|------------|
| 0 | Breaker Close Command | 1 = Close breaker, 0 = Open breaker |
| 1 | Trip Reset | Set to 1 to clear latched trip |
| 2 | AVR Enable | 1 = Voltage regulator active |

**Example:**
`wc 0 1`


Closes the breaker and energizes the feeder.

---

## 🔵 Discrete Inputs (Digital Inputs – Status & Alarms)

(Read-only)

| Address | Name | Meaning |
|----------|------|--------|
| 0 | Breaker Status | 1 = Closed |
| 1 | Trip Active | Protection trip latched |
| 2 | Overcurrent Alarm | Current exceeded limit |
| 3 | Undervoltage Alarm | Voltage too low |
| 4 | Overfrequency Alarm | Frequency too high |
| 5 | Underfrequency Alarm | Frequency too low |

*(Optional: you can extend your client to add a `rd` command for reading DI.)*

---

## 🟡 Holding Registers (Writable Setpoints)

Use command:

`wr address value`


| Addr | Name | Scale | Example |
|------|------|-------|--------|
| 0 | Voltage Setpoint | x1 | 480 = 480V |
| 1 | Load Setpoint | x10 | 350 = 35.0 kW |
| 2 | Frequency Setpoint | x100 | 6000 = 60.00 Hz |
| 3 | Power Factor Setpoint | x1000 | 950 = 0.950 |

**Example:**

`wr 1 600`


Sets load demand to **60.0 kW**

---

## 🔴 Input Registers (Read-Only Measurements)

Use command:

`ri address count`


| Addr | Measurement | Scale | Meaning |
|------|-------------|-------|--------|
| 0 | Voltage (V) | x1 | Line-to-line RMS |
| 1 | Current (A) | x10 | RMS current |
| 2 | Active Power P (kW) | x10 | Real power |
| 3 | Reactive Power Q (kVAR) | x10 | Reactive power |
| 4 | Apparent Power S (kVA) | x10 | Apparent power |
| 5 | Power Factor | x1000 | 0.000–1.000 |
| 6 | Frequency (Hz) | x100 | System frequency |

**Example:**

`ri 0 7`

Output:

`[480, 1234, 350, 150, 380, 950, 5998]`


Interpreted as:

- Voltage = **480 V**
- Current = **123.4 A**
- Active Power = **35.0 kW**
- Reactive Power = **15.0 kVAR**
- Apparent Power = **38.0 kVA**
- Power Factor = **0.950**
- Frequency = **59.98 Hz**

---

# 🖥 Interactive Commands Explained

| Command | What It Does |
|----------|--------------|
| `wc` | Write a coil (digital control signal) |
| `rc` | Read coils (control outputs) |
| `wr` | Write holding register (change setpoint) |
| `rr` | Read holding registers |
| `ri` | Read input registers (measurements) |
| `demo` | Runs automated test sequence |
| `quit` | Exit client |

---

# 🔄 How the Electrical Simulation Behaves

## Breaker Open:

- Current = 0  
- Power = 0  
- Voltage floats near setpoint  

## Breaker Closed:

- Load setpoint determines real power  
- Current calculated from:

`I = S / (√3 × V)`


- Frequency slightly droops with load  
- Voltage droops unless AVR is enabled  

---

## Protection Logic:

- Overcurrent trips breaker  
- Trip latches until reset (`wc 1 1`)  
- Undervoltage and frequency alarms trigger automatically  

---

# 🔎 Typical Demo Sequence

`wc 0 1 # Close breaker
wr 1 500 # Set load to 50.0 kW
wc 2 1 # Enable AVR
ri 0 7 # Read measurements`


Then increase load until overcurrent trip occurs:

`wr 1 2000`


Breaker will trip automatically.

Reset it:

`wc 1 1
wc 0 1`


---

# 🧠 Why This Matters

This mirrors how:

- Substation IEDs expose measurements  
- SCADA systems poll Modbus registers  
- Protection relays trip breakers  
- Operators change setpoints remotely  

It makes your project look like an actual **electrical SCADA simulation**, not just a Python exercise.


## Additional Resources

- Modbus Protocol: https://en.wikipedia.org/wiki/Modbus
- pymodbus Documentation: https://pymodbus.readthedocs.io/
